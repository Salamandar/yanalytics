#!/usr/bin/env python3

import os
from pathlib import Path

import uvicorn

from .app import create_app
from .config import get_config

config_path = Path(os.environ.get("YANALYTICS_CONFIG", "config.yml"))
config = get_config(config_path)

app = create_app(config)


def main() -> None:
    uvicorn.run(
        "yanalytics.asgi:app",
        host=config.server.host,
        port=config.server.port,
        reload=config.testing,
        access_log=config.logging,
    )


if __name__ == "__main__":
    main()
