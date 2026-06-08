#!/usr/bin/env python3

from pathlib import Path

from fastapi import FastAPI


def create_app(config: Path) -> FastAPI:
    app = FastAPI()

    return app
