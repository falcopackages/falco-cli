from __future__ import annotations

import os
import sys
from contextlib import suppress
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


@cappa.command(help="Run your whole django projects in one command.")
class Work:
    def __call__(self) -> None:
        """Run multiple processes in parallel."""

        django_env = {
            **dotenv_values(".env"),
            **os.environ,
            "PYTHONPATH": Path().resolve(strict=True),
            "PYTHONUNBUFFERED": "true",
        }
        commands = {"server": "python manage.py migrate && python manage.py runserver"}

        with suppress(FileNotFoundError):
            pyproject_config = read_toml(Path("pyproject.toml"))
            user_commands = pyproject_config.get("tool", {}).get("falco", {}).get("work", {})
            commands = commands | user_commands

        manager = HonchoManager()

        for name, cmd in commands.items():
            manager.add_process(name, cmd, env=django_env)

        try:
            manager.loop()
        finally:
            manager.terminate()

        sys.exit(manager.returncode)
