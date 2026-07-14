#!/usr/bin/env python3

import os
from pathlib import Path

from .app import create_app
from .config import get_config

config_path = Path(os.environ.get("YANALYTICS_CONFIG", "config.yml"))
config = get_config(config_path)

app = create_app(config)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
