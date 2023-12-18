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

IMPORT_START_COMMENT = "<!-- IMPORTS:START -->"
IMPORT_END_COMMENT = "<!-- IMPORTS:END -->"
CODE_START_COMMENT = "<!-- CODE:START -->"
CODE_END_COMMENT = "<!-- CODE:END -->"


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
    blueprints: Annotated[
        str,
        cappa.Arg(
            default="",
            short="-b",
            long="--blueprints",
            help="The path to custom html templates that will server as blueprints.",
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
            templates_dir = settings.TEMPLATES[0].get("DIRS")[0]
        except IndexError:
            templates_dir = app_folder_path / "templates" / app_label

        model_fields = django_model._meta.get_fields()
        context = {
            "app_label": app_label,
            "model_name": model_name,
            "model_name_plural": f"{model_name}s",
            "model_name_cap": model_name.capitalize(),
            "fields_names": [field.name for field in model_fields],
            "fields_verbose_names": [field.verbose_name for field in model_fields],
        }

        python_blueprints = self.python_blueprints
        hmtl_blueprints = (
            self.html_blueprints
            if not self.blueprints
            else list(Path(self.blueprints).iterdir())
        )

        self.generate_python_code(context=context, blueprints=python_blueprints, app_folder_path=app_folder_path)
        self.generate_html_templates(context=context, blueprints=hmtl_blueprints, templates_dir=templates_dir)

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
    def extract_from(text: str, start_comment: str, end_comment: str):
        start_index = text.find(start_comment) + len(start_comment)
        end_index = text.find(end_comment)
        return text[start_index:end_index]

    def generate_python_code(
        self, app_folder_path: Path, context: dict, blueprints: list[Path]
    ) -> None:
        # blueprints python files end in .py.tpl
        for blueprint in blueprints:
            filecontent = blueprint.read_text()
            imports_template = self.extract_from(
                text=filecontent,
                start_comment=IMPORT_START_COMMENT,
                end_comment=IMPORT_END_COMMENT,
            )
            code_template = self.extract_from(
                text=filecontent,
                start_comment=CODE_START_COMMENT,
                end_comment=CODE_END_COMMENT,
            )
            file_to_write_to = ".".join(blueprint.name.split(".")[:-1])
            file_to_write_to = app_folder_path / file_to_write_to
            file_to_write_to.touch(exist_ok=True)
            rendered_imports = self.render_to_string(imports_template, context)
            rendered_code = self.render_to_string(code_template, context)
            file_to_write_to.write_text(rendered_imports + file_to_write_to.read_text() + rendered_code)
            self.run_formatters(str(file_to_write_to))

    def generate_html_templates(self, context: dict, blueprints: list[Path], templates_dir:Path) -> None:
        pass

    @property
    def python_blueprints(self) -> list[Path]:
        files = ["views.py.tpl", "forms.py.tpl"]
        return [get_falco_blueprints_path() /"crud" / file for file in files]

    @property
    def html_blueprints(self) -> list[Path]:
        files = ["create.html", "detail.html", "list.html", "update.html"]
        return [get_falco_blueprints_path() /"crud"/ file for file in files]

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
    def render_to_string(template_content: str, context: dict):
        return Template(template_content).render(Context(context))

    @staticmethod
    def run_formatters(filepath: str):
        autoflake = [
            "autoflake",
            "--in-place",
            "--remove-all-unused-imports",
            filepath,
        ]
        black = ["black", filepath]
        isort = ["isort", filepath]
        subprocess.run(autoflake)
        subprocess.run(isort)
        subprocess.run(black)
