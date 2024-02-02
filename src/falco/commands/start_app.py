import subprocess
from pathlib import Path
from typing import Annotated

import cappa
import parso
from falco.commands.crud.utils import run_python_formatters
from falco.utils import get_project_name
from falco.utils import run_in_shell
from falco.utils import simple_progress


def get_settings_file_path() -> str:
    from django.conf import settings

    s = settings.SETTINGS_MODULE
    s = s.replace(".", "/")
    return f"{s}.py"


@cappa.command(help="Initialize a new django app the falco way.")
class StartApp:
    app_name: Annotated[str, cappa.Arg(help="Name of the app to create.")]

    def __call__(self, project_name: Annotated[str, cappa.Dep(get_project_name)]):
        apps_dir = Path() / project_name
        app_dir = apps_dir / self.app_name

        final_app_name = f"{project_name}.{self.app_name}"

        try:
            app_dir.mkdir()
        except FileExistsError as e:
            msg = f"Python module with the name {self.app_name} already exists in {apps_dir}."
            raise cappa.Exit(msg, code=1) from e

        with simple_progress(f"Creating {self.app_name} app"):
            result = subprocess.run(
                ["python", "manage.py", "startapp", self.app_name, app_dir],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                msg = result.stderr.replace("CommandError:", "")
                raise cappa.Exit(msg, code=1)

            (app_dir / "tests.py").unlink()

            model_name = self.app_name[:-1].capitalize() if self.app_name.endswith("s") else self.app_name.capitalize()

            models_file = app_dir / "models.py"

            models_file.write_text(
                f"""
from django.db import models
from model_utils.models import TimeStampedModel

class {model_name}(TimeStampedModel):
    name=models.CharField(max_length=255)
"""
            )

            (app_dir / "admin.py").write_text("")

            (app_dir / "views.py").write_text("")

            app_config_file = app_dir / "apps.py"
            app_config_file.write_text(app_config_file.read_text().replace(self.app_name, final_app_name))

        run_python_formatters(models_file)
        run_python_formatters(self.register_app(app_name=final_app_name))

    @simple_progress("Registering app")
    def register_app(self, app_name: str) -> Path:
        names = ["LOCAL_APPS", "INSTALLED_APPS"]

        settings_file = Path(run_in_shell(get_settings_file_path, eval_result=False))

        module = parso.parse(settings_file.read_text())

        for node in module.children:
            try:
                if (
                    node.children[0].type == parso.python.tree.ExprStmt.type
                    and node.children[0].children[0].value in names
                ):
                    apps = node.children[0].children[2]
                    elements = apps.children[1]

                    elements.children.append(parso.parse(f"'{app_name}',"))
                    new_content = module.get_code()
                    settings_file.write_text(new_content)
                    break
            except AttributeError:
                continue

        return settings_file
