from pathlib import Path
from typing import Annotated

import cappa
from falco import checks
from falco.utils import get_project_name
from falco.utils import run_in_shell
from falco.utils import simple_progress
from rich import print as rich_print


def get_django_debug_value() -> bool:
    from django.conf import settings

    return settings.DEBUG


@cappa.command(help="Remove all migrations for the specified applications directory, intended only for development.")
class RmMigrations:
    apps_dir: Annotated[
        Path | None,
        cappa.Arg(default=None, help="The path to your django apps directory."),
    ]
    skip_git_check: Annotated[
        bool,
        cappa.Arg(
            default=False,
            long="--skip-git-check",
            help="Do not check if your git repo is clean.",
        ),
    ]

    def __call__(self, project_name: Annotated[str, cappa.Dep(get_project_name)]):
        checks.clean_git_repo(ignore_dirty=self.skip_git_check)

        django_debug_value = run_in_shell(get_django_debug_value, eval_result=True)
        if not django_debug_value:
            raise cappa.Exit(
                "Nope, not happening, this command can only be run with DEBUG=True.",
                code=1,
            )

        if not self.apps_dir:
            self.apps_dir = Path() / project_name

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
