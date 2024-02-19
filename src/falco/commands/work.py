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
        current_dir = Path().resolve()

        django_env = {
            **os.environ,
            "PYTHONPATH": str(current_dir),
            "PYTHONUNBUFFERED": "true",
            **parse_dotenv(current_dir / ".env"),
        }

        commands = self.get_commands()
        manager = Manager()

        for name, cmd in commands.items():
            manager.add_process(name, cmd, env=django_env)

        try:
            manager.loop()
        finally:
            manager.terminate()

        sys.exit(manager.returncode)

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
