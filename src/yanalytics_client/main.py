#!/usr/bin/env python3

import argparse
import hashlib
from pathlib import Path

import requests

from .config import get_config


class YanalyticsInstance:
    def __init__(self, server: str, machine_id: str | None) -> None:
        self.server = server
        self.uuid = self._uuid(machine_id)

    def _raise_err(self, response: requests.Response) -> None:
        if not response.ok:
            msg: str | dict[str, str] = response.json()
            if isinstance(msg, dict):
                msg = msg["error"]
            raise RuntimeError(msg)

    def _uuid(self, machine_id: str | None) -> str:
        salt = "yunohost-analytics"
        machine_id = machine_id or Path("/etc/machine-id").read_text().strip()
        return hashlib.sha512((salt + machine_id).encode()).hexdigest()

    def push_stats(self) -> None:
        data: dict[str, str | dict[str, str]] = {
            "uuid": self.uuid,
            "versions": {
                "debian": "",
                "yunohost": "",
            },
        }
        url = f"{self.server}/api/v1/instance/analytic"
        response = requests.post(url, json=data, timeout=60)
        self._raise_err(response)

    def instance_delete(self) -> None:
        data = {"uuid": str(self.uuid)}
        url = f"{self.server}/api/v1/instance"
        response = requests.delete(url, params=data, timeout=60)
        self._raise_err(response)


def show_analytics(server: str) -> None:
    pass


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--server", type=str, help="Yanalytics server", required=False
    )
    parser.add_argument("-c", "--config", type=Path, help="Configuration file")

    sub = parser.add_subparsers(required=True, dest="mode")
    parser_inst = sub.add_parser("instance")
    parser_inst.add_argument("-i", "--machine-id", type=str, required=False)
    parser_inst.add_argument("action", type=str, choices=["push", "delete"])

    sub.add_parser("analytics")

    args = parser.parse_args()

    config = get_config(args.config)

    server = args.server or config.analytics_server
    if "://" not in server:
        server = f"https://{server}"

    match args.mode:
        case "instance":
            instance = YanalyticsInstance(server, args.machine_id or config.machine_id)
            match args.action:
                case "push":
                    instance.push_stats()
                case "delete":
                    instance.instance_delete()

        case "analytics":
            show_analytics(server)


if __name__ == "__main__":
    main()
