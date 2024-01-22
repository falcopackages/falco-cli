import os
import sys
from contextlib import suppress
from pathlib import Path

import cappa
from dotenv import load_dotenv
from honcho.manager import Manager
from tomlkit import parse


@cappa.command(help="Run your whole django projects in one command.")
class Work:
    def __call__(self) -> None:
        """Run multiple processes in parallel."""

        current_dir = Path().resolve()
        django_env = {
            **os.environ,
            "PYTHONPATH": str(current_dir),
            "PYTHONUNBUFFERED": "true",
        }

        load_dotenv(current_dir / ".env")

        commands = {"server": "python manage.py migrate && python manage.py runserver"}

        with suppress(FileNotFoundError):
            # TODO: put this logic in FalcoConfig
            pyproject_config = parse(Path("pyproject.toml").read_text())
            user_commands = pyproject_config.get("tool", {}).get("falco", {}).get("work", {})
            commands |= user_commands

        manager = Manager()

        for name, cmd in commands.items():
            manager.add_process(name, cmd, env=django_env)

        try:
            manager.loop()
        finally:
            manager.terminate()

        sys.exit(manager.returncode)
