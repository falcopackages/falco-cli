import os
import sys
from contextlib import suppress
from pathlib import Path

import cappa
from dotenv import load_dotenv
from honcho.manager import Manager


try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


def read_toml(file: Path) -> dict:
    return tomllib.loads(file.read_text())


# class Popen(HonchoPopen):
#     def __init__(self, cmd, **kwargs):
#         kwargs.setdefault("start_new_session", False)
#         super().__init__(cmd, **kwargs)


# class Process(HonchoProcess):
#     def __init__(self, cmd, name=None, colour=None, quiet=False, env=None, cwd=None):
#         super().__init__(cmd, name, colour, quiet, env, cwd)
#         self._child_ctor = Popen


# class Manager(HonchoManager):
#     def __init__(self, printer=None):
#         super().__init__(printer=printer)
#         self._process_ctor = Process


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
            pyproject_config = read_toml(Path("pyproject.toml"))
            user_commands = pyproject_config.get("tool", {}).get("falco", {}).get("work", {})
            commands = commands | user_commands

        manager = Manager()

        for name, cmd in commands.items():
            manager.add_process(name, cmd, env=django_env)

        try:
            manager.loop()
        finally:
            manager.terminate()

        sys.exit(manager.returncode)
