from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Annotated

import cappa
from dict_deep import deep_get
from dotenv import dotenv_values
from honcho.manager import Manager as HonchoManager

from falco.utils import get_current_dir_as_project_name, read_toml


def _get_venv_directory() -> str | None:
    patterns = ["venv", ".venv"]
    for p in patterns:
        path = Path(p)
        if path.exists() and (path / "bin/python").exists():
            return p


def _get_user_commands(file: Path) -> dict:
    try:
        config = read_toml(file)
        return deep_get(config, "tool.cuzzy.work") or {}
    except FileNotFoundError:
        return {}


def _get_redis_command(django_env: dict) -> str | None:
    redis_url = django_env.get("REDIS_URL", "")
    if "localhost" in redis_url or "127.0.0.1" in redis_url:
        redis_port = redis_url.split(":")[-1].split("/")[0]
        return f"redis-server --port {redis_port}"


def _get_tailwind_command(pyproject_file: Path, project_name: str) -> str | None:
    config = read_toml(pyproject_file)
    dependencies = deep_get(config, "tool.poetry.dependencies") or {}
    if "pytailwindcss" in dependencies:
        return f"tailwindcss -i {project_name}/static/css/input.css -o {project_name}/static/css/output.css --watch"


def _update_command_with_venv(venv_dir: str | None, cmd: str) -> str:
    # TODO: this could also be done with other scripts like celery or arq
    return f"{venv_dir}/bin/{cmd}" if venv_dir and cmd.startswith("python") else cmd


@cappa.command(help="Run multiple processes in parallel.")
class Work:
    pyproject_file: Annotated[
        Path,
        cappa.Arg(
            default=Path("pyproject.toml"),
            hidden=True,
        ),
    ]
    project_name: Annotated[str, cappa.Arg(default="", parse=get_current_dir_as_project_name, hidden=True)]

    def __call__(
        self,
    ) -> None:
        """Run multiple processes in parallel."""

        django_env = {
            **dotenv_values(".env"),
            **os.environ,
            "PYTHONPATH": Path().resolve(strict=True),
            "PYTHONUNBUFFERED": "true",
        }

        venv_dir = _get_venv_directory()

        migrate_cmd = _update_command_with_venv(venv_dir, "python manage.py migrate")
        runserver_cmd = _update_command_with_venv(venv_dir, "python manage.py runserver --nostatic")
        commands = {
            "server": f"{migrate_cmd} && {runserver_cmd}",
        }

        if redis_cmd := _get_redis_command(django_env):
            commands["redis"] = redis_cmd

        if self.pyproject_file.exists():
            if tailwind_cmd := _get_tailwind_command(self.pyproject_file, self.project_name):
                commands["tailwind"] = tailwind_cmd

        user_commands = _get_user_commands(self.pyproject_file)

        user_commands = {k: _update_command_with_venv(venv_dir, v) for k, v in user_commands.items()}

        commands |= user_commands

        manager = HonchoManager()

        for name, cmd in commands.items():
            manager.add_process(name, cmd, env=django_env)

        manager.loop()

        sys.exit(manager.returncode)
