import subprocess
from pathlib import Path
from typing import Annotated
from typing import cast
from typing import TypedDict

import cappa
from falco.utils import get_falco_blueprints_path
from falco.utils import run_shell_command
from falco.utils import simple_progress
from rich import print as rich_print

IMPORT_START_COMMENT = "<!-- IMPORTS:START -->"
IMPORT_END_COMMENT = "<!-- IMPORTS:END -->"
CODE_START_COMMENT = "<!-- CODE:START -->"
CODE_END_COMMENT = "<!-- CODE:END -->"


class DjangoModelContext(TypedDict):
    app_label: str
    model_name: str
    model_name_plural: str
    model_name_lower: str
    fields_names: list[str]
    fields_verbose_names: list[str]


class DjangoModel(TypedDict):
    model_name: str
    model_fields_names: list[str]
    model_fields_verbose_names: list[str]


class DjangoModelWithContext(DjangoModel):
    context: DjangoModelContext


models_data_code = """
from django.apps import apps
models = apps.get_app_config("{}").get_models()
exclude_fields = {}
model_name = lambda model: model.__name__
model_fields_names = lambda model: [field.name for field in model._meta.fields if field.name not in exclude_fields]
model_fields_verbose_names = lambda model: [field.verbose_name for field in model._meta.fields if field.name not in exclude_fields]
print([{{"model_name": model_name(model), "model_fields_names": model_fields_names(model), "model_fields_verbose_names": model_fields_verbose_names(model)}} for model in models])
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


def extract_content_from(text: str, start_comment: str, end_comment: str):
    start_index = text.find(start_comment) + len(start_comment)
    end_index = text.find(end_comment)
    return text[start_index:end_index]


def get_urls(model_name_lower: str, model_name_plural: str) -> str:
    return f"""
        path('{model_name_plural}/', views.{model_name_lower}_list, name='{model_name_lower}_list'),
        path('{model_name_plural}/create/', views.{model_name_lower}_create, name='{model_name_lower}_create'),
        path('{model_name_plural}/<int:pk>/', views.{model_name_lower}_detail, name='{model_name_lower}_detail'),
        path('{model_name_plural}/<int:pk>/update/', views.{model_name_lower}_update, name='{model_name_lower}_update'),
        path('{model_name_plural}/<int:pk>/delete/', views.{model_name_lower}_delete, name='{model_name_lower}_delete'),
    """


def render_to_string(template_content: str, context: dict):
    return run_shell_command(
        django_render_template_code.format(template_content, context),
        eval_result=False,
    )


@simple_progress("Running python formatters")
def run_python_formatters(filepath: str):
    autoflake = [
        "autoflake",
        "--in-place",
        "--remove-all-unused-imports",
        filepath,
    ]
    black = ["black", filepath]
    isort = ["isort", filepath]
    subprocess.run(autoflake, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(isort, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(black, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


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
    excluded_fields: Annotated[
        list[str],
        cappa.Arg(short=True, default=[], long="--exclude", help="Fields to exclude."),
    ]
    only_python: Annotated[
        bool,
        cappa.Arg(default=False, long="--only-python", help="Generate only python."),
    ]
    only_html: Annotated[bool, cappa.Arg(default=False, long="--only-html", help="Generate only html.")]
    entry_point: Annotated[
        bool,
        cappa.Arg(default=False, long="--entry-point", help="Use the specified model as the entry point of the app."),
    ]

    def __call__(self):
        v = self.model_path.split(".")
        if len(v) == 1:
            model_name = None
            app_label = v[0]
        else:
            model_name = v.pop()
            app_label = ".".join(v)

        if self.entry_point and not model_name:
            raise cappa.Exit("The --entry-point option requires a full model path.", code=1)

        with simple_progress("Getting models info"):
            all_django_models = cast(
                list[DjangoModelWithContext],
                run_shell_command(models_data_code.format(app_label, self.excluded_fields)),
            )

            app_folder_path, templates_dir = cast(
                tuple[str, str],
                run_shell_command(app_path_and_templates_dir_code.format(app_label, app_label)),
            )

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

        updated_python_files = set()

        python_blueprints = get_blueprints_ending_in(".py.bp")
        hmtl_blueprints = list(Path(self.html_blueprints).iterdir()) or get_blueprints_ending_in(".html")

        django_models_with_context: list[DjangoModelWithContext] = []
        for django_model in django_models:
            model_name = django_model.get("model_name")
            model_name_lower = model_name.lower()
            model_name_plural = f"{model_name_lower}s"
            context = {
                "app_label": app_label,
                "model_name": model_name,
                "model_name_plural": model_name_plural,
                "model_name_lower": model_name_lower,
                "fields_names": django_model.get("model_fields_names"),
                "fields_verbose_names": django_model.get("model_fields_verbose_names"),
            }
            django_models_with_context.append(
                {
                    **django_model,
                    "context": context,
                }
            )

        if not self.only_html:
            updated_python_files.update(
                self.generate_python_code(
                    app_label=app_label,
                    context=context,
                    blueprints=python_blueprints,
                    app_folder_path=app_folder_path,
                    django_models_with_context=django_models_with_context,
                    entry_point=self.entry_point,
                )
            )
        if not self.only_python:
            self.generate_html_templates(
                context=context,
                blueprints=hmtl_blueprints,
                templates_dir=templates_dir,
            )

        for file in updated_python_files:
            run_python_formatters(str(file))

        display_names = ", ".join(m.get("model_name") for m in django_models)
        rich_print(f"[green] CRUD views generated for: {display_names}[/green]")

    @simple_progress("Generating python code")
    def generate_python_code(
        self,
        app_label: str,
        app_folder_path: Path,
        context: dict,
        blueprints: list[Path],
        django_models_with_context: list[DjangoModelWithContext],
        entry_point: bool,
    ) -> list[Path]:
        updated_files = []
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

            imports_content = ""
            code_content = ""
            urls_content = ""

            for django_model in django_models_with_context:
                context = django_model.get("context")
                imports_content += render_to_string(imports_template, context)
                code_content += render_to_string(code_template, context)
                urls_content += get_urls(
                    model_name_lower=context.get("model_name_lower"),
                    model_name_plural=context.get("model_name_plural"),
                )
                if entry_point:
                    urls_content = urls_content.replace(f"{context.get('model_name_plural')}/", "")
                    urls_content = urls_content.replace(f"list", "index")
                    urls_content = urls_content.replace(f"{context.get('model_name_lower')}_", "")
                    code_content = code_content.replace(f"{context.get('model_name_lower')}_", "")
                    code_content = code_content.replace(f"list", "index")

            file_to_write_to.write_text(imports_content + file_to_write_to.read_text() + code_content)
            updated_files.append(file_to_write_to)

        app_urls = app_folder_path / "urls.py"
        if app_urls.exists():
            urlpatterns = f"\nurlpatterns +=[{urls_content}]"
            app_urls.write_text(app_urls.read_text() + urlpatterns)
        else:
            app_urls.touch()
            app_urls.write_text(self._initial_urls_content(app_label, urls_content))
        updated_files.append(app_urls)
        return updated_files

    def _initial_urls_content(self, app_label: str, urls_content: str) -> str:
        return f"""
from django.urls import path
from . import views

app_name = "{app_label}"

urlpatterns = [
{urls_content}
]
        """

    @simple_progress("Generating html templates")
    def generate_html_templates(self, context: dict, blueprints: list[Path], templates_dir: Path) -> None:
        pass
