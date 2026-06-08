#!/usr/bin/env python3

import os
from pathlib import Path

from .app import create_app

config = Path(os.environ.get("YANALYTICS_CONFIG", "config.yml"))

if not config.exists():
    raise RuntimeError(f"Configuration file {config} does not exist!")

app = create_app(config)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
