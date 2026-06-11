#!/usr/bin/env python3

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .database import Statistic, YanalyticsDatabase


def create_app(config: Path) -> FastAPI:
    logger = logging.getLogger()

    database = YanalyticsDatabase()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
        database.initialize()
        yield

    app = FastAPI(debug=True, lifespan=lifespan)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
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

    # Push a new statistic
    @app.post("/api/v1/instance/statistic", status_code=201)
    def post_statistic(item: Statistic) -> dict:
        logger.debug("Getting statistic %s", item)
        return {"message":"Item created successfully","item":item}

    @app.delete("/api/v1/instance", status_code=202)
    def delete_machine(uuid: str) -> dict:
        logger.debug("Deleting machine %s", uuid)
        return {}

    @app.get("api/v1/analytics/instances")
    def instances_count() -> dict[Literal["instances"], int]:
        return {"instances": 0}


    return app
