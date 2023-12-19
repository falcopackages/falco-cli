from pathlib import Path
from typing import Annotated

import cappa
from falco.utils import run_shell_command
from falco.utils import simple_progress
from rich import print as rich_print

django_debug_value_code = """
from django.conf import settings
print(settings.DEBUG)
"""


@cappa.command(help="Remove all migrations for the specified applications directory, intended only for development.")
class RmMigrations:
    apps_dir: Annotated[Path, cappa.Arg(help="The path to your django apps directory.")]

    def __call__(self):
        django_debug_value = run_shell_command(django_debug_value_code, eval_result=True)
        if not django_debug_value:
            raise cappa.Exit("This command can only be run with DEBUG=True.", code=1)

        apps = set()
        with simple_progress("Removing migration files"):
            for folder in self.apps_dir.iterdir():
                migration_dir = folder / "migrations"
                if not migration_dir.exists():
                    continue
                apps.add(folder.stem)
                for file in migration_dir.iterdir():
                    if file.suffix == ".py" and file.name not in ["__init__.py"]:
                        file.unlink()
        apps_ = ", ".join(apps)
        rich_print(f"[green] Removed migration files for apps: {apps_}")
