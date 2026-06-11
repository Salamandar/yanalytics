#!/usr/bin/env python3

from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, ValidationError

model_config = ConfigDict(
    validate_default=True,
    extra="forbid",
)


class ConfigAnalytics(BaseModel):
    model_config = model_config

    hardware: bool = True
    geo: bool = True
    apps: bool = True
    users: bool = True
    domains: bool = True


class Config(BaseModel):
    model_config = model_config

    analytics_server: str = "https://analytics.yunohost.org"
    machine_id: str | None = None
    analytics: ConfigAnalytics = ConfigAnalytics()

    testing: bool = False

    def __init__(self, path: Path) -> None:
        try:
            config = yaml.safe_load(path.open("r"))
            super().__init__(**config)

        except FileNotFoundError:
            raise RuntimeError(f"Config file {path} not found!") from None

        except yaml.YAMLError as err:
            raise RuntimeError(
                f"Config file {path} has invalid YAML syntax:\n{err}"
            ) from None

        except ValidationError as err:
            raise RuntimeError(f"Invalid config file {path}:\n{err}") from None
