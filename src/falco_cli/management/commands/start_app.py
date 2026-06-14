from pathlib import Path

import parso
from django.conf import settings
from django.core.management import CommandError
from django.core.management import call_command
from django.core.management.base import BaseCommand
from falco_cli.management.base import get_apps_dir
from falco_cli.utils import run_python_formatters
from falco_cli.utils import simple_progress


class Command(BaseCommand):
    help = "Initialize a new django app the falco way."

    def add_arguments(self, parser):
        parser.add_argument("app_name", type=str, help="Name of the app to create.")

    def handle(self, *_, **options):
        app_name = options["app_name"]
        apps_dir = get_apps_dir()
        app_dir = apps_dir / app_name
        final_app_name = f"{apps_dir.name}.{app_name}".strip(".").lower()

        try:
            app_dir.mkdir()
        except FileExistsError as e:
            msg = f"Python module with the name {app_name} already exists in {apps_dir}."
            raise CommandError(msg) from e

        self.create_app(app_name=app_name, app_dir=app_dir, final_app_name=final_app_name)
        self.register_app(app_name=final_app_name)

    @classmethod
    def create_app(cls, app_name: str, app_dir: Path | None, final_app_name: str):
        with simple_progress(f"Creating {app_name} app"):
            call_command("startapp", app_name, str(app_dir))

            (app_dir / "tests.py").unlink()

            model_name = app_name[:-1].capitalize() if app_name.endswith("s") else app_name.capitalize()

            models_file = app_dir / "models.py"

            models_file.write_text(
                f"""
from django.db import models


class {model_name}(models.Model):
    name=models.CharField(max_length=255)

    def __str__(self):
        return self.name
"""
            )

            (app_dir / "admin.py").write_text("")

            (app_dir / "views.py").write_text("")

            app_config_file = app_dir / "apps.py"
            app_config_file.write_text(app_config_file.read_text().replace(app_name, final_app_name))

        run_python_formatters(models_file)

    @simple_progress("Registering app")
    def register_app(self, app_name: str):
        names = ["LOCAL_APPS", "INSTALLED_APPS"]

        settings_file = Path(settings.SETTINGS_MODULE.replace(".", "/") + ".py")

        module = parso.parse(settings_file.read_text())

        for node in module.children:
            try:
                if (
                    node.children[0].type == parso.python.tree.ExprStmt.type
                    and node.children[0].children[0].value in names
                ):
                    apps = node.children[0].children[2]
                    elements = apps.children[1]

                    elements.children.append(parso.parse(f",\n    '{app_name}',"))
                    new_content = module.get_code()
                    settings_file.write_text(new_content)
                    break
            except AttributeError:
                continue
        run_python_formatters(settings_file)
