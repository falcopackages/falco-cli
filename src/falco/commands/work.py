from __future__ import annotations

import os
import sys
from pathlib import Path

import cappa
from dotenv import dotenv_values
from honcho.manager import Manager as HonchoManager

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


def read_toml(file: Path) -> dict:
    return tomllib.loads(file.read_text())


@cappa.command(help="Run multiple processes in parallel.")
class Work:
    def __call__(self) -> None:
        """Run multiple processes in parallel."""

        django_env = {
            **dotenv_values(".env"),
            **os.environ,
            "PYTHONPATH": Path().resolve(strict=True),
            "PYTHONUNBUFFERED": "true",
        }

        try:
            pyproject_config = read_toml(Path("pyproject.toml"))
            commands = pyproject_config.get("tool", {}).get("falco", {}).get("work", {})
        except FileNotFoundError as e:
            raise cappa.Exit(
                "The pyproject.toml file could not be found. ", code=1
            ) from e

        if not commands:
            raise cappa.Exit("No commands were found in the pyproject.toml file. ")

        manager = HonchoManager()

        for name, cmd in commands.items():
            manager.add_process(name, cmd, env=django_env)

        manager.loop()

        sys.exit(manager.returncode)
