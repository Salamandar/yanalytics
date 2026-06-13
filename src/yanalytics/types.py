from pydantic import BaseModel, ConfigDict

model_config = ConfigDict(
    validate_default=True,
    extra="forbid",
)


class HWAnalytics(BaseModel):
    arch: str
    cpus: int
    ram: int
    disk: int


class VersionsAnalytics(BaseModel):
    debian: str
    yunohost: str


class Analytic(BaseModel):
    uuid: str
    versions: VersionsAnalytics
    hardware: HWAnalytics | None = None
    geocode: str | None = None
    apps: list[str] | None = None
    users_nb: int | None = None
    domains_nb: int | None = None


class AnalyticsAggregate(BaseModel):
    # Timestamped number of instances
    instances: list[tuple[int, int]]
