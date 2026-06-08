#!/usr/bin/env python3

import logging
from pathlib import Path
from typing import Literal

from fastapi import FastAPI

from .database import Statistic


def create_app(config: Path) -> FastAPI:
    app = FastAPI(debug=True)

    logger = logging.getLogger()

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
