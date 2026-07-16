#!/usr/bin/env python3

import datetime
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from functools import cache

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import Config
from .database import YanalyticsDatabase
from .types import Analytic, AnalyticsAggregate


def create_app(config: Config) -> FastAPI:
    logger = logging.getLogger()

    database = YanalyticsDatabase(config.database)

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
        database.initialize()
        yield

    app = FastAPI(debug=config.testing, lifespan=lifespan)

    if config.testing:
        origins = ["*"]
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.frontend("/", directory=config.server.frontend)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        _: Request, exc: RequestValidationError
    ) -> JSONResponse:
        def join_error_loc(loc: list[str]) -> str:
            if loc[0] == "body":
                loc[0] = ""
            return ".".join(loc)

        errors = {
            error["type"]: join_error_loc(list(error["loc"])) for error in exc.errors()
        }
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"error": {"input_data": errors}}),
        )

    # Push a new analytic
    @app.post("/api/v1/instance/analytic", status_code=201)
    async def post_analytic(item: Analytic) -> dict[str, str | Analytic]:
        logger.debug("Getting analytic %s", item)
        await database.insert_analytics(item)
        return {"message": "Item created successfully", "item": item}

    @app.delete("/api/v1/instance", status_code=202)
    async def delete_machine(uuid: str) -> dict[str, str]:
        logger.debug("Deleting machine %s", uuid)
        await database.delete_machine(uuid)
        return {}

    @cache
    async def compute_analytics_data() -> AnalyticsAggregate:
        data = AnalyticsAggregate(
            instances=[],
            apps={},
            versions={},
            arch={},
            cpus={},
            ram={},
            disk={},
            users={},
            domains={},
        )

        # TODO save json?
        return data

    @app.get("/api/v1/analytics/all")
    async def analytics() -> AnalyticsAggregate:
        return await compute_analytics_data()

    @app.get("/api/v1/analytics/stats")
    async def analytics_stats():
        return {
            "instances": [
                {"year": 2010, "v12": 40, "v13": 10},
                {"year": 2011, "v12": 30, "v13": 15},
                {"year": 2012, "v12": 20, "v13": 20},
                {"year": 2013, "v12": 15, "v13": 25},
                {"year": 2014, "v12": 10, "v13": 30},
                {"year": 2015, "v12": 8, "v13": 35},
                {"year": 2016, "v12": 6, "v13": 40},
            ],
            "apps_nb": [
                {"year": 2010, "count": 100},
                {"year": 2011, "count": 105},
                {"year": 2012, "count": 200},
                {"year": 2013, "count": 205},
                {"year": 2014, "count": 300},
                {"year": 2015, "count": 305},
                {"year": 2016, "count": 400},
            ],
        }

    @app.get("/api/v1/analytics/apps")
    async def analytics_apps():
        apps = [
            {"id": "nextcloud", "name": "Nextcloud", "count": 2367, "percent": 90},
            {"id": "vaultwarden", "name": "Vaultwarden", "count": 1987, "percent": 70},
            {"id": "my_webapp", "name": "My Webapp", "count": 1000, "percent": 40},
        ] * 100

        def lundi(i: int) -> str:
            start = datetime.date(2018, 1, 1)
            delta = datetime.timedelta(days=7 * i)
            return (start + delta).strftime("%Y-%m-%d")

        count_history = {lundi(i): i + 100 for i in range(440)}

        return {
            "details": apps,
            "count_history": count_history,
        }

    if config.testing:

        @app.post("/api/v1/analytics/sync")
        async def recompute_analytics_data() -> None:
            compute_analytics_data.cache_clear()
            await compute_analytics_data()

    return app
