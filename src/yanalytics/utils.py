#!/usr/bin/env python3

import logging
import shutil
import subprocess
from collections.abc import Callable
from functools import cache


def if_not_none[T](func: Callable[[T], T]) -> Callable[[T | None], T | None]:
    def wrapper(arg: T | None) -> T | None:
        return None if arg is None else func(arg)

    return wrapper


@if_not_none
def reduce_version_yunohost(version: str) -> str:
    # Only save x.y
    return ".".join(version.split(".", 2)[0:2])


@if_not_none
def reduce_arch(arch: str) -> str:
    # Nothing smart for now
    return arch


@if_not_none
def reduce_version_debian(version: str) -> int:
    # Only save major
    return int(version.split(".", 1)[0])


@if_not_none
def reduce_bytes(size: int) -> int:
    # Kinda-smart-repartition
    # We want for example 1.75GB seen as 2GB and not 1GB
    log2 = (size + int(size / 7)).bit_length() - 1
    return 2**log2


@if_not_none
def reduce_cpus(cpus: int) -> int:
    # Nothing smart for now
    return cpus


@if_not_none
def reduce_users_nb(users: int) -> int:
    # round to power of 2
    return 2 ** users.bit_length()


@if_not_none
def reduce_domains_nb(domains: int) -> int:
    # Nothing smart for now
    return domains


@cache
def geoip_check() -> bool:
    # Print only once
    if not shutil.which("geoiplookup"):
        logging.error("Tool geoiplookup not installed!")
        return False
    return True


@if_not_none
def geoip(ip: str) -> str | None:
    if not geoip_check():
        return None

    cmd = "geoiplookup" + ("6" if ":" in ip else "")
    result = subprocess.check_output([cmd, ip]).decode()
    return result.split(":")[1].split(",")[0].strip()
