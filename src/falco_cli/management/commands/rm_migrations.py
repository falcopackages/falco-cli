from pathlib import Path

from falco_cli.management.base import CleanRepoOnlyCommand
from falco_cli.management.base import exit_if_debug_false
from falco_cli.management.base import get_apps_dir
from falco_cli.utils import simple_progress


class Command(CleanRepoOnlyCommand):
    help = "Remove all migrations for the specified applications directory, intended only for development."

    def handle(self, *_, **__):
        exit_if_debug_false()
        apps_dir = get_apps_dir()
        apps = self.delete_migration_files(apps_dir=apps_dir)
        self.stdout.write(self.style.SUCCESS(f"Removed migration files for apps: {', '.join(apps)}"))

    @classmethod
    def delete_migration_files(cls, apps_dir: Path) -> set[str]:
        apps = set()
        with simple_progress("Removing migration files"):
            for folder in apps_dir.iterdir():
                migration_dir = folder / "migrations"
                if not migration_dir.exists():
                    continue
                apps.add(folder.stem)
                for file in migration_dir.iterdir():
                    if file.suffix == ".py" and file.name not in ["__init__.py"]:
                        file.unlink()
        return apps
