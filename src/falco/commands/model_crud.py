import os
import subprocess
import sys
from pathlib import Path
from typing import Annotated

import cappa
import django
from django.apps import apps
from django.conf import settings
from django.template.engine import Context
from django.template.engine import Template
from falco.utils import get_falco_blueprints_path


@cappa.command(
    help="Generate CRUD (Create, Read, Update, Delete) views for a model.", name="crud"
)
class ModelCRUD:
    model_path: Annotated[
        str,
        cappa.Arg(
            help="The path (<app_label>.<model name>) of the model to generate CRUD views for. Ex: myapp.product"
        ),
    ]
    settings_module: Annotated[
        str,
        cappa.Arg(
            default="config.settings",
            help="The django settings module to use.",
            short="-s",
            long="--settings",
        ),
    ]

    def __call__(self):
        sys.path.insert(0, str(Path()))
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", self.settings_module)
        django.setup()

        if "." not in self.model_path:
            raise cappa.Exit(f"Invalid model path {self.model_path}", code=1)
        v = self.model_path.split(".")
        model_name = v.pop()
        app_label = ".".join(v)

        try:
            django_app = apps.get_app_config(app_label=app_label)
        except LookupError as e:
            raise cappa.Exit(f"App {app_label} not found", code=1) from e

        try:
            django_model = django_app.get_model(model_name)
        except LookupError as exc:
            raise cappa.Exit(
                f"Model {model_name} not found in app {app_label}", code=1
            ) from exc

        app_folder_path = Path(django_app.path)

        try:
            settings.TEMPLATES[0].get("DIRS")[0]
        except IndexError:
            app_folder_path / "templates" / app_label

        model_fields = django_model._meta.get_fields()
        context = {
            "app_label": app_label,
            "model_name": model_name,
            "model_name_plural": f"{model_name}s",
            "model_name_cap": model_name.capitalize(),
            "fields_names": [field.name for field in model_fields],
            "fields_verbose_names": [field.verbose_name for field in model_fields],
        }
        print(context)

        crud_blueprints_path = get_falco_blueprints_path() / "crud"

        # render python files
        views = self.render_to_string(crud_blueprints_path / "views.py.tpl", context)
        forms = self.render_to_string(crud_blueprints_path / "forms.py.tpl", context)

        # TODO: separate import and always insert them first
        views_py = app_folder_path / "views.py"
        views_py.touch(exist_ok=True)
        views_py.write_text(views_py.read_text() + views)
        self.run_formatters(str(views_py))

        forms_py = app_folder_path / "forms.py"
        forms_py.touch(exist_ok=True)
        forms_py.write_text(forms_py.read_text() + forms)
        self.run_formatters(str(forms_py))

        urls_py = app_folder_path / "urls.py"
        if urls_py.exists():
            # append new_urls to the end
            pass
        else:
            # create file
            # add app_name
            # add urls
            pass
        # render html files

    @staticmethod
    def get_urls(model_name: str) -> list[str]:
        return [
            f"path('{model_name}/', views.{model_name}_list, name='{model_name}_list'),",
            f"path('{model_name}/create/', views.{model_name}_create, name='{model_name}_create'),",
            f"path('{model_name}/<int:pk>/', views.{model_name}_detail, name='{model_name}_detail'),",
            f"path('{model_name}/<int:pk>/update/', views.{model_name}_update, name='{model_name}_update'),",
            f"path('{model_name}/<int:pk>/delete/', views.{model_name}_delete, name='{model_name}_delete'),",
        ]

    @staticmethod
    def render_to_string(filepath: Path, context: dict):
        return Template(filepath.read_text()).render(Context(context))

    @staticmethod
    def run_formatters(filepath: str):
        autoflake = [
            "autoflake",
            "--in-place",
            "--remove-all-unused-imports",
            filepath,
        ]
        black = ["black", filepath]
        subprocess.run(autoflake)
        subprocess.run(black)
