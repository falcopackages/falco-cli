import os
import sys
from pathlib import Path
from typing import Annotated

import cappa
from falco.config import read_falco_config
from honcho.manager import Manager

from .sync_dotenv import parse as parse_dotenv

default_server_cmd = "python manage.py migrate && python manage.py runserver {address}"
default_address = "127.0.0.1:8000"


@cappa.command(help="Run your whole django projects in one command.")
class Work:
    address: Annotated[str, cappa.Arg(default=default_address, help="Django server address")] = default_address

    def __call__(self) -> None:
        commands = self.get_commands()
        manager = Manager()

        django_env = self.resolve_django_env()

        for name, cmd in commands.items():
            manager.add_process(name, cmd, env=django_env)

        try:
            manager.loop()
        finally:
            manager.terminate()

        sys.exit(manager.returncode)

    def resolve_django_env(self) -> dict:
        current_dir = Path().resolve()
        env_file = current_dir / ".env"
        env_vars = parse_dotenv(env_file.read_text()) if env_file.exists() else {}

        return {
            **os.environ,
            "PYTHONPATH": str(current_dir),
            "PYTHONUNBUFFERED": "true",
            **env_vars,
        }

    def get_commands(self) -> dict:
        commands = {"server": default_server_cmd}

        pyproject_file = Path("pyproject.toml")

        if pyproject_file.exists():
            user_commands = read_falco_config(pyproject_path=pyproject_file).get("work", {})
        else:
            user_commands = {}

        commands["server"] = commands["server"].format(address=self.address)
        commands |= user_commands

        return commands
