import subprocess
from pathlib import Path
from typing import Annotated
from typing import TypedDict

import cappa
import parso
from falco import checks
from falco.config import CRUDConfig
from falco.config import read_falco_config
from falco.utils import get_project_name
from falco.utils import RICH_ERROR_MARKER
from falco.utils import RICH_INFO_MARKER
from falco.utils import RICH_SUCCESS_MARKER
from falco.utils import run_in_shell
from falco.utils import simple_progress
from rich import print as rich_print

from .install_crud_utils import InstallCrudUtils
from .utils import extract_python_file_templates
from .utils import get_crud_blueprints_path
from .utils import render_to_string
from .utils import run_html_formatters
from .utils import run_python_formatters


@cappa.command(help="Generate CRUD (Create, Read, Update, Delete) views for a model.", name="crud")
class ModelCRUD:
    model_path: Annotated[
        str,
        cappa.Arg(
            help="The path (<app_label>.<model_name>) of the model to generate CRUD views for. Ex: myapp.product"
        ),
    ]
    blueprints: Annotated[
        str,
        cappa.Arg(
            default="",
            long="--blueprints",
            help="The path to custom html templates that will serve as blueprints.",
        ),
    ]
    excluded_fields: Annotated[
        list[str],
        cappa.Arg(
            short=True,
            default=[],
            long="--exclude",
            help="Fields to exclude from the views, forms and templates.",
        ),
    ]
    only_python: Annotated[
        bool,
        cappa.Arg(default=False, long="--only-python", help="Generate only python code."),
    ]
    only_html: Annotated[
        bool,
        cappa.Arg(default=False, long="--only-html", help="Generate only html code."),
    ]
    entry_point: Annotated[
        bool,
        cappa.Arg(
            default=False,
            long="--entry-point",
            help="Use the specified model as the entry point of the app.",
        ),
    ]
    login_required: Annotated[
        bool,
        cappa.Arg(
            default=False,
            short="-l",
            long="--login-required",
            help="Add the login_required decorator to all views.",
        ),
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
        pyproject_path = Path("pyproject.toml")
        falco_config = read_falco_config(pyproject_path=pyproject_path) if pyproject_path.exists() else {}
        crud_config: CRUDConfig = falco_config.get("crud", {})

        self.blueprints = crud_config.get("blueprints", self.blueprints)
        self.login_required = crud_config.get("login_required", self.login_required)
        self.skip_git_check = crud_config.get("skip_git_check", self.skip_git_check)

        checks.clean_git_repo(ignore_dirty=self.skip_git_check)

        v = self.model_path.split(".")

        if len(v) == 1:
            name = None
            app_label = v[0]
        else:
            name = v.pop()
            app_label = ".".join(v)

        if crud_config.get("always_migrate", False):
            commands = [
                f"python manage.py makemigrations {app_label}",
                f"python manage.py migrate {app_label}",
            ]
            with simple_progress("Running migrations"):
                for cmd in commands:
                    result = subprocess.run(cmd.split(), capture_output=True, check=False, text=True)

                    if result.returncode != 0:
                        msg = result.stderr
                        raise cappa.Exit("migrations step failed\n" + msg, code=1)

        if self.entry_point and not name:
            raise cappa.Exit("The --entry-point option requires a full model path.", code=1)

        with simple_progress("Getting models info"):
            all_django_models = run_in_shell(
                get_models_data,
                app_label=app_label,
                excluded_fields=self.excluded_fields,
            )

            app_folder_path_str, app_name, templates_dir_str = run_in_shell(
                get_app_path_name_and_templates_dir, app_label=app_label
            )

            app_folder_path = Path(app_folder_path_str)
            templates_dir = Path(templates_dir_str)

        django_models = (
            [m for m in all_django_models if m["name"].lower() == name.lower()] if name else all_django_models
        )
        if name and not django_models:
            msg = f"Model {name} not found in app {app_label}"
            raise cappa.Exit(msg, code=1)

        python_blueprint_context: list[PythonBlueprintContext] = []
        html_blueprint_context: list[HtmlBlueprintContext] = []
        install_path, crud_utils_installed = InstallCrudUtils.get_install_path(
            project_name=project_name,
            falco_config=falco_config,
        )
        crud_utils_import = str(install_path).replace("/", ".")

        for django_model in django_models:
            python_blueprint_context.append(
                get_python_blueprint_context(
                    project_name=project_name,
                    app_label=app_label,
                    django_model=django_model,
                    crud_utils_import=crud_utils_import,
                    login_required=self.login_required,
                )
            )
            html_blueprint_context.append(get_html_blueprint_context(app_label=app_label, django_model=django_model))

        updated_python_files = set()

        if not self.only_html:
            python_blueprints = list((get_crud_blueprints_path() / "python").iterdir())
            updated_python_files.update(
                self.generate_python_code(
                    app_label=app_label,
                    blueprints=python_blueprints,
                    app_folder_path=app_folder_path,
                    contexts=python_blueprint_context,
                    entry_point=self.entry_point,
                )
            )

            updated_python_files.update(
                self.generating_urls(
                    app_name=app_name,
                    app_folder_path=app_folder_path,
                    app_label=app_label,
                    django_models=django_models,
                    entry_point=self.entry_point,
                )
            )

        updated_html_files = set()
        if not self.only_python:
            html_blueprints = (
                list(Path(self.blueprints).glob("*.html.jinja"))
                if self.blueprints
                else list((get_crud_blueprints_path() / "html").iterdir())
            )

            updated_html_files.update(
                self.generate_html_templates(
                    contexts=html_blueprint_context,
                    entry_point=self.entry_point,
                    blueprints=html_blueprints,
                    templates_dir=templates_dir,
                )
            )

        for file in updated_python_files:
            run_python_formatters(str(file))

        for file in updated_html_files:
            run_html_formatters(str(file))

        display_names = ", ".join(m.get("name") for m in django_models)
        rich_print(f"{RICH_SUCCESS_MARKER}CRUD views generated for: {display_names}[/green]")
        if not crud_utils_installed:
            rich_print(
                f"{RICH_INFO_MARKER}It appears that your CRUD utilities have not been installed yet. "
                f"Please execute the command 'falco install-crud-utils' to install them."
            )

    @simple_progress("Generating python code")
    def generate_python_code(
        self,
        app_label: str,
        app_folder_path: Path,
        blueprints: list[Path],
        contexts: list["PythonBlueprintContext"],
        *,
        entry_point: bool,
    ) -> list[Path]:
        updated_files = []

        for blueprint in blueprints:
            imports_template, code_template = extract_python_file_templates(blueprint.read_text())
            # blueprints python files end in .py.jinja
            file_name_without_jinja = ".".join(blueprint.name.split(".")[:-1])
            file_to_write_to = app_folder_path / file_name_without_jinja
            file_to_write_to.touch(exist_ok=True)

            imports_content, code_content = "", ""

            for context in contexts:
                model_name_lower = context["model_name"].lower()
                imports_content += render_to_string(imports_template, context)
                code_content += render_to_string(code_template, context)

                if entry_point:
                    code_content = code_content.replace(f"{model_name_lower}_", "")
                    code_content = code_content.replace("list", "index")

            file_to_write_to.write_text(imports_content + file_to_write_to.read_text() + code_content)
            updated_files.append(file_to_write_to)

        model_name = contexts[0]["model_name"] if len(contexts) == 1 else None
        updated_files.append(
            register_models_in_admin(
                app_folder_path=app_folder_path,
                app_label=app_label,
                model_name=model_name,
            )
        )
        return updated_files

    @simple_progress("Generating urls")
    def generating_urls(
        self,
        app_folder_path: Path,
        app_label: str,
        app_name: str,
        django_models: list["DjangoModel"],
        *,
        entry_point: bool,
    ) -> list[Path]:
        urls_content = ""
        for django_model in django_models:
            model_name_lower = django_model["name"].lower()
            urlsafe_model_verbose_name_plural = django_model["verbose_name_plural"].lower().replace(" ", "-")
            urls_content += get_urls(
                model_name_lower=model_name_lower,
                urlsafe_model_verbose_name_plural=urlsafe_model_verbose_name_plural,
            )
            if entry_point:
                urls_content = urls_content.replace(f"{urlsafe_model_verbose_name_plural}/", "")
                urls_content = urls_content.replace("list", "index")
                urls_content = urls_content.replace(f"{model_name_lower}_", "")

        app_urls = app_folder_path / "urls.py"
        updated_files = [app_urls]
        if app_urls.exists():
            urlpatterns = f"\nurlpatterns +=[{urls_content}]"
            app_urls.write_text(app_urls.read_text() + urlpatterns)
        else:
            app_urls.touch()
            app_urls.write_text(initial_urls_content(app_label, urls_content))
            updated_files.append(register_app_urls(app_label=app_label, app_name=app_name))
        return updated_files

    @simple_progress("Generating html templates")
    def generate_html_templates(
        self,
        templates_dir: Path,
        blueprints: list[Path],
        contexts: list["HtmlBlueprintContext"],
        *,
        entry_point: bool,
    ) -> list[Path]:
        updated_files = []
        templates_dir.mkdir(exist_ok=True, parents=True)
        for blueprint in blueprints:
            filecontent = blueprint.read_text()

            for context in contexts:
                model_name_lower = context["model_name"].lower()
                new_filename = f"{model_name_lower}_{blueprint.name.replace('.jinja', '')}"
                if entry_point:
                    new_filename = blueprint.name.replace(".jinja", "")
                if new_filename.startswith("list"):
                    new_filename = new_filename.replace("list", "index")
                file_to_write_to = templates_dir / new_filename
                file_to_write_to.touch(exist_ok=True)
                views_content = render_to_string(filecontent, context=context)

                if entry_point:
                    views_content = views_content.replace(f"{model_name_lower}_", "")
                    views_content = views_content.replace("list", "index")
                file_to_write_to.write_text(views_content)
                updated_files.append(file_to_write_to)

        return updated_files


class PythonBlueprintContext(TypedDict):
    project_name: str
    login_required: bool
    app_label: str
    model_name: str
    model_verbose_name_plural: str
    model_fields: dict[str, str]
    crud_utils_import: str


class UrlsForContext(TypedDict):
    list_view_url: str
    create_view_url: str
    detail_view_url: str
    update_view_url: str
    delete_view_url: str


class HtmlBlueprintContext(UrlsForContext):
    app_label: str
    model_name: str
    model_verbose_name_plural: str
    model_fields: dict[str, str]
    # a example of the dict: {"Name": "{{product.name}}", "Price": "{{product.price}}"}
    fields_verbose_name_with_accessor: dict[str, str]


class DjangoField(TypedDict):
    verbose_name: str
    editable: str


class DjangoModel(TypedDict):
    name: str
    verbose_name_plural: str
    fields: dict[str, DjangoField]


def get_models_data(app_label: str, excluded_fields: list[str]) -> "list[DjangoModel]":
    from django.apps import apps

    models = apps.get_app_config(app_label).get_models()

    def get_model_dict(model) -> "DjangoModel":
        name = model.__name__
        verbose_name_plural = getattr(model._meta, "verbose_name_plural", f"{name}s")
        fields: dict[str, "DjangoField"] = {
            field.name: {"verbose_name": field.verbose_name, "editable": field.editable}
            for field in model._meta.fields
            if field.name not in excluded_fields
        }
        return {
            "name": name,
            "fields": fields,
            "verbose_name_plural": verbose_name_plural,
        }

    return [get_model_dict(model) for model in models]


def get_app_path_name_and_templates_dir(app_label: str) -> tuple[str, str, str]:
    from django.apps import apps
    from django.conf import settings
    from pathlib import Path

    app = apps.get_app_config(app_label)
    dirs = settings.TEMPLATES[0].get("DIRS", [])
    templates_dir = Path(dirs[0]) if dirs else Path(app.path) / "templates"
    app_templates_dir = templates_dir / app_label
    return str(app.path), str(app.name), str(app_templates_dir)


def get_root_url_config_path() -> str:
    from django.conf import settings

    return settings.ROOT_URLCONF


def get_urls(model_name_lower: str, urlsafe_model_verbose_name_plural: str) -> str:
    prefix = urlsafe_model_verbose_name_plural
    return f"""
        path('{prefix}/', views.{model_name_lower}_list, name='{model_name_lower}_list'),
        path('{prefix}/create/', views.{model_name_lower}_create, name='{model_name_lower}_create'),
        path('{prefix}/<int:pk>/', views.{model_name_lower}_detail, name='{model_name_lower}_detail'),
        path('{prefix}/<int:pk>/update/', views.{model_name_lower}_update, name='{model_name_lower}_update'),
        path('{prefix}/<int:pk>/delete/', views.{model_name_lower}_delete, name='{model_name_lower}_delete'),
    """


def get_urls_template_string(app_label: str, model_name_lower: str) -> UrlsForContext:
    return {
        "list_view_url": f"{{% url '{app_label}:{model_name_lower}_list' %}}",
        "create_view_url": f"{{% url '{app_label}:{model_name_lower}_create' %}}",
        "detail_view_url": f"{{% url '{app_label}:{model_name_lower}_detail' {model_name_lower}.pk %}}",
        "update_view_url": f"{{% url '{app_label}:{model_name_lower}_update' {model_name_lower}.pk %}}",
        "delete_view_url": f"{{% url '{app_label}:{model_name_lower}_delete' {model_name_lower}.pk %}}",
    }


def initial_urls_content(app_label: str, urls_content: str) -> str:
    return f"""
from django.urls import path
from . import views

app_name = "{app_label}"

urlpatterns = [
{urls_content}
]
        """


def register_app_urls(app_label: str, app_name: str) -> Path:
    root_url = run_in_shell(get_root_url_config_path, eval_result=False)
    root_url = root_url.strip().replace(".", "/")
    rool_url_path = Path(f"{root_url}.py")
    module = parso.parse(rool_url_path.read_text())
    new_path = parso.parse(f"path('{app_label}/', include('{app_name}.urls', namespace='{app_label}'))")

    for node in module.children:
        try:
            if (
                node.children[0].type == parso.python.tree.ExprStmt.type
                and node.children[0].children[0].value == "urlpatterns"
            ):
                patterns = node.children[0].children[2]
                elements = patterns.children[1]
                elements.children.append(new_path)
                new_content = module.get_code()
                new_content = "from django.urls import include\n" + new_content
                rool_url_path.write_text(new_content)
                break
        except AttributeError:
            continue

    return rool_url_path


def register_models_in_admin(app_folder_path: Path, app_label: str, model_name: str | None = None) -> Path:
    admin_file = app_folder_path / "admin.py"
    admin_file.touch(exist_ok=True)
    cmd_args = [app_label]
    if model_name:
        cmd_args.append(model_name)

    result = subprocess.run(
        ["python", "manage.py", "admin_generator", *cmd_args],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        msg = result.stderr.split("\n")[-2]
        rich_print(f"{RICH_ERROR_MARKER}Admin failed to generate: {msg}")
        return admin_file

    # the first set the encoding, it is useless
    admin_code = result.stdout.split("\n", 1)[1]
    admin_file.write_text(admin_file.read_text() + admin_code)

    if not model_name:
        # we probably don't need to reorder the imports if the admin code is being generated for all models
        return admin_file

    # if this is not the first time running this, the imports will be messed up, move all
    # of them to the top
    admin_lines = admin_file.read_text().split("\n")
    _imports = []
    _code = []
    for line in admin_lines:
        if line.startswith("from"):
            _imports.append(line)
        else:
            _code.append(line)
    admin_file.write_text("\n" + "\n".join(_imports) + "\n" + "\n".join(_code))

    return admin_file


def get_python_blueprint_context(
    project_name: str,
    app_label: str,
    django_model: DjangoModel,
    crud_utils_import: str,
    *,
    login_required: bool,
) -> PythonBlueprintContext:
    return {
        "project_name": project_name,
        "app_label": app_label,
        "login_required": login_required,
        "model_name": django_model["name"],
        "model_verbose_name_plural": django_model["verbose_name_plural"],
        "model_fields": django_model["fields"],
        "crud_utils_import": crud_utils_import,
    }


def get_html_blueprint_context(app_label: str, django_model: DjangoModel) -> HtmlBlueprintContext:
    model_name_lower = django_model["name"].lower()
    return {
        "app_label": app_label,
        "model_name": django_model["name"],
        "model_verbose_name_plural": django_model["verbose_name_plural"],
        "model_fields": django_model["fields"],
        "fields_verbose_name_with_accessor": {
            field_data["verbose_name"]: "{{" + f"{model_name_lower}.{field_name}" + "}}"
            for field_name, field_data in django_model["fields"].items()
        },
        **get_urls_template_string(
            app_label=app_label,
            model_name_lower=django_model["name"].lower(),
        ),
    }
