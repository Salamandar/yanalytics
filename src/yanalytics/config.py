#!/usr/bin/env python3

import tomllib
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, ValidationError


class CustomModel(BaseModel):
    model_config = ConfigDict(
        validate_default=True,
        extra="forbid",
    )


class Config(CustomModel):
    database: Path

    testing: bool = False


def get_config(path: Path) -> Config:
    try:
        if path.name.endswith((".yaml", ".yml")):
            data = yaml.safe_load(path.open("r"))
        elif path.name.endswith(".toml"):
            data = tomllib.load(path.open("rb"))
        else:
            raise RuntimeError(f"Could not determine format of config {path}")
        config = Config(**data)
    except FileNotFoundError:
        raise RuntimeError(f"Config file {path} not found!") from None
    except yaml.YAMLError as err:
        msg = f"Config file {path} has invalid YAML syntax:\n{err}"
        raise RuntimeError(msg) from None
    except tomllib.TOMLDecodeError as err:
        msg = f"Config file {path} has invalid TOML syntax:\n{err}"
        raise RuntimeError(msg) from None
    except ValidationError as err:
        raise RuntimeError(f"Invalid config file {path}:\n{err}") from None
    else:
        return config
