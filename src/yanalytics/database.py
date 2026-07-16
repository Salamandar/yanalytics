#!/usr/bin/env python3

import datetime
import logging
from pathlib import Path

import sqlalchemy as sa
import sqlalchemy.exc
from sqlalchemy.orm import (
    # Mapped,
    Session,
    declarative_base,
    # mapped_column,
    relationship,
)

from . import utils
from .types import Analytic

Base = declarative_base()


# class Domain(Base):
#     __tablename__ = "domains"
#     name: Mapped[str] = mapped_column(primary_key=True, unique=True)
#     key: Mapped[bytes] = mapped_column(sa.BLOB, nullable=False)
#     password: Mapped[str] = mapped_column(nullable=True, default=None)
#     last_query: Mapped[int] = mapped_column(default=0)


# Association table for many-to-many Instance <-> App
instance_apps = sa.Table(
    "instance_apps",
    Base.metadata,
    sa.Column(
        "instance_id", sa.String(36), sa.ForeignKey("instances.uuid"), primary_key=True
    ),
    sa.Column("app_id", sa.Integer, sa.ForeignKey("apps.name"), primary_key=True),
)


def _timestamp_default() -> datetime.datetime:
    return datetime.datetime.now(datetime.UTC)


class InstanceAnalytics(Base):
    __tablename__ = "instances"

    uuid = sa.Column(sa.String(36), primary_key=True, unique=True)
    timestamp = sa.Column(sa.DateTime(timezone=False), default=_timestamp_default)

    # Versions
    debian_version = sa.Column(sa.String(64), nullable=True)
    yunohost_version = sa.Column(sa.String(64), nullable=True)

    # Hardware
    arch = sa.Column(sa.String(16), nullable=True)
    cpus = sa.Column(sa.Integer, nullable=True)
    ram_mb = sa.Column(sa.Integer, nullable=True)
    disk_gb = sa.Column(sa.Integer, nullable=True)

    # Geocode can be a string (e.g. "FR") or JSON with more details
    geocode = sa.Column(sa.String(5), nullable=True)

    # many-to-many -> installed apps
    apps = relationship("App", secondary=instance_apps, back_populates="instances")

    # basic counts
    users_nb = sa.Column(sa.Integer, nullable=True)
    domains_nb = sa.Column(sa.Integer, nullable=True)


class App(Base):
    __tablename__ = "apps"

    name = sa.Column(sa.String(255), unique=True, nullable=False, primary_key=True)
    instances = relationship(
        "InstanceAnalytics", secondary=instance_apps, back_populates="apps"
    )


class YanalyticsDatabase:
    def __init__(self, db_path: Path) -> None:
        self.log = logging.getLogger("yanalytics")
        self.db_path = db_path

    def initialize(self) -> None:
        sqlite_url = f"sqlite:///{self.db_path}"

        connect_args = {"check_same_thread": False}
        self.engine = sa.create_engine(sqlite_url, connect_args=connect_args)

        with self.engine.connect() as conn:
            stmt = sa.text("pragma user_version")
            stmt_set_version = sa.text("pragma user_version = 2")
            current_version: int = conn.execute(stmt).scalar_one()
            self.log.debug("DB is at version %d", current_version)

            if current_version == 0:
                self.log.info("Creating database...")
                Base.metadata.create_all(self.engine)
                conn.execute(stmt_set_version)

            conn.commit()

    async def insert_analytics(self, analytic: Analytic) -> None:

        db_analytic = InstanceAnalytics(
            uuid=analytic.uuid,
            timestamp=_timestamp_default(),
            debian_version=utils.reduce_version_debian(analytic.versions.debian),
            yunohost_version=utils.reduce_version_yunohost(analytic.versions.yunohost),
            arch=utils.reduce_arch(
                analytic.hardware.arch if analytic.hardware else None
            ),
            cpus=utils.reduce_cpus(
                analytic.hardware.cpus if analytic.hardware else None
            ),
            ram_mb=utils.reduce_bytes(
                analytic.hardware.ram if analytic.hardware else None
            ),
            disk_gb=utils.reduce_bytes(
                analytic.hardware.disk if analytic.hardware else None
            ),
            geocode=utils.geoip(analytic.geocode),
            apps=analytic.apps or [],
            users_nb=utils.reduce_users_nb(analytic.users_nb),
            domains_nb=utils.reduce_domains_nb(analytic.domains_nb),
        )

        with Session(self.engine) as session:
            session.merge(db_analytic)
            session.commit()

    async def delete_machine(self, uuid: str) -> None:
        self.log.info("Deleting %s", uuid)
        with Session(self.engine) as session:
            stmt = sa.delete(InstanceAnalytics).where(InstanceAnalytics.uuid == uuid)
            session.execute(stmt)
            session.commit()

    async def aggregate(self) -> None:
        pass
        # now = _timestamp_default()
        # with Session(self.engine) as session:
        #     instances_nb = session.query(InstanceAnalytics).count()

        #     pass
