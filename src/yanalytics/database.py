#!/usr/bin/env python3

from pydantic import BaseModel
from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select

class HWStatistics(BaseModel):
    arch: str
    cpus: int
    ram: int
    disk: int


class VersionsStatistics(BaseModel):
    debian: str
    yunohost: str


class Statistic(BaseModel):
    uuid: str
    versions: VersionsStatistics
    hardware: HWStatistics | None = None
    geocode: str | None = None
    apps: list[str] | None = None
    users_nb: int | None = None
    domains_nb: int | None = None


class YanalyticsDatabase:
    pass
