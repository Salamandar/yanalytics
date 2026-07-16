#!/usr/bin/env python3

import tomllib
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


def get_config(path: Path) -> Config:
    try:
        if path.name.endswith((".yaml", ".yml")):
            data = yaml.safe_load(path.open("r"))
        elif path.name.endswith(".toml"):
            data = tomllib.load(path.open("rb"))
        else:
            msg = f"Could not determine format of config {path}"
            raise RuntimeError(msg)
        config = Config(**data)
    except FileNotFoundError:
        msg = f"Config file {path} not found!"
        raise RuntimeError(msg) from None
    except yaml.YAMLError as err:
        msg = f"Config file {path} has invalid YAML syntax:\n{err}"
        raise RuntimeError(msg) from None
    except tomllib.TOMLDecodeError as err:
        msg = f"Config file {path} has invalid TOML syntax:\n{err}"
        raise RuntimeError(msg) from None
    except ValidationError as err:
        msg_0 = f"Invalid config file {path}:\n{err}"
        raise RuntimeError(msg_0) from None
    else:
        return config
