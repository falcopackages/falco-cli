import subprocess
from pathlib import Path
from typing import Annotated
from typing import TypedDict

import cappa
from falco.utils import get_falco_blueprints_path
from rich import print as rich_print

IMPORT_START_COMMENT = "<!-- IMPORTS:START -->"
IMPORT_END_COMMENT = "<!-- IMPORTS:END -->"
CODE_START_COMMENT = "<!-- CODE:START -->"
CODE_END_COMMENT = "<!-- CODE:END -->"


class DjangoModel(TypedDict):
    model_name: str
    model_fields_names: list[str]
    model_fields_verbose_names: list[str]


models_data_code = """
from django.apps import apps
models = apps.get_app_config("{}").get_models()
print([{{'model_name': model.__name__, 'model_fields_names': [field.name for field in model._meta.fields], 'model_fields_verbose_names': [field.verbose_name for field in model._meta.fields]}} for model in models])
"""

app_path_and_templates_dir_code = """
from django.apps import apps
from django.conf import settings
from pathlib import Path
app = apps.get_app_config("{}")
dirs = settings.TEMPLATES[0].get("DIRS", [])
templates_dir = Path(dirs[0]) if dirs else Path(app.path) / "templates"
app_templates_dir = templates_dir / "{}"
print((str(app.path), str(app_templates_dir)))
"""

django_render_template_code = """
from django.template.engine import Context, Template
print(Template('''{}''').render(Context({})))
"""


def run_shell_command(command: str, eval_result: bool = True):
    result = subprocess.run(
        ["python", "manage.py", "shell", "-c", command],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise Exception(result.stderr)
    return eval(result.stdout) if eval_result else result.stdout


def extract_content_from(text: str, start_comment: str, end_comment: str):
    start_index = text.find(start_comment) + len(start_comment)
    end_index = text.find(end_comment)
    return text[start_index:end_index]


def get_urls(model_name_lower: str) -> list[str]:
    return [
        f"path('{model_name_lower}/', views.{model_name_lower}_list, name='{model_name_lower}_list'),",
        f"path('{model_name_lower}/create/', views.{model_name_lower}_create, name='{model_name_lower}_create'),",
        f"path('{model_name_lower}/<int:pk>/', views.{model_name_lower}_detail, name='{model_name_lower}_detail'),",
        f"path('{model_name_lower}/<int:pk>/update/', views.{model_name_lower}_update, name='{model_name_lower}_update'),",
        f"path('{model_name_lower}/<int:pk>/delete/', views.{model_name_lower}_delete, name='{model_name_lower}_delete'),",
    ]


def render_to_string(template_content: str, context: dict):
    return run_shell_command(
        django_render_template_code.format(template_content, context),
        eval_result=False,
    )


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


def get_blueprints_ending_in(file_ext: str) -> str:
    return [file for file in (get_falco_blueprints_path() / "crud").iterdir() if file.name.endswith(file_ext)]


@cappa.command(help="Generate CRUD (Create, Read, Update, Delete) views for a model.", name="crud")
class ModelCRUD:
    model_path: Annotated[
        str,
        cappa.Arg(
            help="The path (<app_label>.<model name>) of the model to generate CRUD views for. Ex: myapp.product"
        ),
    ]
    html_blueprints: Annotated[
        str,
        cappa.Arg(
            default="",
            long="--html-blueprints",
            help="The path to custom html templates that will server as blueprints.",
        ),
    ]
    only_python: Annotated[
        bool,
        cappa.Arg(default=False, long="--only-python", help="Generate only python."),
    ]
    only_html: Annotated[bool, cappa.Arg(default=False, long="--only-html", help="Generate only html.")]

    def __call__(self):
        v = self.model_path.split(".")
        if len(v) == 1:
            model_name = None
            app_label = v[0]
        else:
            model_name = v.pop()
            app_label = ".".join(v)

        all_django_models: list[DjangoModel] = run_shell_command(models_data_code.format(app_label))
        app_folder_path, templates_dir = run_shell_command(app_path_and_templates_dir_code.format(app_label, app_label))
        app_folder_path = Path(app_folder_path)
        templates_dir = Path(templates_dir)

        if model_name:
            for django_model in all_django_models:
                if django_model["model_name"].lower() == model_name.lower():
                    django_models = [django_model]
                    break
            else:
                raise cappa.Exit(f"Model {model_name} not found in app {app_label}", code=1)
        else:
            django_models = all_django_models

        for django_model in django_models:
            model_name = django_model.get("model_name")
            context = {
                "app_label": app_label,
                "model_name": model_name,
                "model_name_plural": f"{model_name}s",
                "model_name_lower": model_name.lower(),
                "fields_names": django_model.get("model_fields_names"),
                "fields_verbose_names": django_model.get("model_fields_verbose_names"),
            }

            python_blueprints = get_blueprints_ending_in(".py.bp")
            hmtl_blueprints = list(Path(self.html_blueprints).iterdir()) or get_blueprints_ending_in(".html")

            if not self.only_html:
                self.generate_python_code(
                    context=context,
                    blueprints=python_blueprints,
                    app_folder_path=app_folder_path,
                )
            if not self.only_python:
                self.generate_html_templates(
                    context=context,
                    blueprints=hmtl_blueprints,
                    templates_dir=templates_dir,
                )

        display_names = ", ".join(m.get("model_name") for m in django_models)
        rich_print(f"[green] CRUD views generated for: {display_names}[/green]")

    def generate_python_code(self, app_folder_path: Path, context: dict, blueprints: list[Path]) -> None:
        # blueprints python files end in .py.bp
        for blueprint in blueprints:
            filecontent = blueprint.read_text()
            imports_template = extract_content_from(
                text=filecontent,
                start_comment=IMPORT_START_COMMENT,
                end_comment=IMPORT_END_COMMENT,
            )
            code_template = extract_content_from(
                text=filecontent,
                start_comment=CODE_START_COMMENT,
                end_comment=CODE_END_COMMENT,
            )
            file_to_write_to = ".".join(blueprint.name.split(".")[:-1])
            file_to_write_to = app_folder_path / file_to_write_to
            file_to_write_to.touch(exist_ok=True)
            rendered_imports = render_to_string(imports_template, context)
            rendered_code = render_to_string(code_template, context)
            file_to_write_to.write_text(rendered_imports + file_to_write_to.read_text() + rendered_code)
            run_formatters(str(file_to_write_to))

    def generate_html_templates(self, context: dict, blueprints: list[Path], templates_dir: Path) -> None:
        pass
