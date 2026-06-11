#!/usr/bin/env python3

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

from fastapi import FastAPI

from .database import Statistic, YanalyticsDatabase


def create_app(config: Path) -> FastAPI:
    logger = logging.getLogger()

    database = YanalyticsDatabase()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
        database.initialize()
        yield

    app = FastAPI(debug=True, lifespan=lifespan)

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
