from io import StringIO
from pathlib import Path
from typing import TypedDict

import parso
from django.apps import AppConfig
from django.apps import apps
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import CommandError
from django.template import Context
from django.template import Template
from falco_cli.management.base import CleanRepoOnlyCommand
from falco_cli.management.commands.copy_template import get_template_absolute_path
from falco_cli.utils import run_html_formatters
from falco_cli.utils import run_python_formatters
from falco_cli.utils import simple_progress

IMPORT_START_COMMENT = "# IMPORTS:START"
IMPORT_END_COMMENT = "# IMPORTS:END"
CODE_START_COMMENT = "# CODE:START"
CODE_END_COMMENT = "# CODE:END"


class DjangoField(TypedDict):
    verbose_name: str
    editable: bool
    class_name: str
    accessor: str  # e.g: {{product.name}}


class DjangoModel(TypedDict):
    name: str
    name_lower: str
    name_plural: str
    lookup_field: str
    path_converter: str
    verbose_name: str
    verbose_name_plural: str
    fields: dict[str, DjangoField]
    obj_accessor: str
    has_file_field: bool
    has_editable_date_field: bool


class BlueprintContext(TypedDict):
    login_required: bool
    entry_point: bool
    app_label: str
    model: DjangoModel
    fields_tuple: str
    editable_fields_tuple: str
    view_name_prefix: str
    list_view_name: str
    detail_view_name: str
    delete_view_name: str
    list_view_url: str
    create_view_url: str
    detail_view_url: str
    update_view_url: str
    delete_view_url: str
    table_block: str
    pagination_block: str
    ordering: str


class Command(CleanRepoOnlyCommand):
    help = "Generate CRUD (Create, Read, Update, Delete) views for a model."

    def add_arguments(self, parser):
        parser.add_argument(
            "model_path",
            type=str,
            help="The path (<app_label>.<model_name>) of the model to generate CRUD views for. Ex: myapp.product",
        )
        parser.add_argument(
            "-e",
            "--exclude",
            action="append",
            help="Fields to exclude from the views, forms and templates.",
        )
        parser.add_argument("--only-python", action="store_true", help="Generate only python code.")
        parser.add_argument("--only-html", action="store_true", help="Generate only html code.")
        parser.add_argument(
            "--entry-point",
            action="store_true",
            help="Use the specified model as the entry point of the app.",
        )
        parser.add_argument(
            "--login-required",
            "-l",
            action="store_true",
            help="Add the login_required decorator to all views.",
        )
        parser.add_argument(
            "--migrate",
            "-m",
            action="store_true",
            help="Run makemigrations and migrate beforehand",
        )
        parser.add_argument(
            "--order-by",
            type=str,
            default=None,
            help="Field to order querysets by (default: model's lookup_field)",
        )
        parser.add_argument(
            "--no-admin",
            action="store_true",
            help="Skip admin.py generation",
        )
    def handle(self, *_, **options):
        model_path = options["model_path"]
        excluded_fields = options["exclude"] or []
        only_python = options["only_python"]
        only_html = options["only_html"]
        entry_point = options["entry_point"]
        login_required = options["login_required"]
        migrate = options["migrate"]
        order_by = options["order_by"]
        self.no_admin = options["no_admin"]

        model_path_parts = model_path.split(".")
        if len(model_path_parts) == 1:
            model_name = None
            app_label = model_path_parts[0]
        else:
            model_name = model_path_parts.pop()
            app_label = ".".join(model_path_parts)

        if entry_point and not model_name:
            msg = "The --entry-point option requires a full model path."
            raise CommandError(msg)

        if migrate:
            with simple_progress("Running migrations"):
                call_command("makemigrations", app_label)
                call_command("migrate")

        app: AppConfig = apps.get_app_config(app_label)
        with simple_progress("Getting models info"):
            all_django_models = self.get_models_data(
                app_label=app_label,
                excluded_fields=excluded_fields,
                entry_point=entry_point,
            )
            dirs = settings.TEMPLATES[0].get("DIRS", [])
            templates_dir = Path(dirs[0]) / app_label if dirs else Path(app.path) / "templates"

        django_models = (
            [m for m in all_django_models if m["name"].lower() == model_name.lower()]
            if model_name
            else all_django_models
        )
        if model_name and not django_models:
            msg = f"Model {model_name} not found in app {app_label}"
            raise CommandError(msg)

        blueprint_contexts: list[BlueprintContext] = [
            build_blueprint_context(
                app_label=app_label,
                django_model=django_model,
                login_required=login_required,
                entry_point=entry_point,
                order_by=order_by,
            )
            for django_model in django_models
        ]

        updated_python_files = set()

        if not only_html:
            python_blueprints = ("crud/forms.py.dtl", "crud/views.py.dtl")
            updated_python_files.update(
                self.generate_python_code(
                    app=app,
                    blueprints=[Path(get_template_absolute_path(p)) for p in python_blueprints],
                    contexts=blueprint_contexts,
                )
            )

            updated_python_files.update(
                self.generating_urls(
                    app=app,
                    django_models=django_models,
                    entry_point=entry_point,
                )
            )

        updated_html_files = set()
        if not only_python:
            html_blueprints = ("crud/list.html", "crud/form.html", "crud/detail.html")
            updated_html_files.update(
                self.generate_html_templates(
                    contexts=blueprint_contexts,
                    entry_point=entry_point,
                    blueprints=[Path(get_template_absolute_path(p)) for p in html_blueprints],
                    templates_dir=templates_dir,
                )
            )

        with simple_progress("Running python formatters"):
            for file in updated_python_files:
                run_python_formatters(str(file))

        with simple_progress("Running html formatters"):
            for file in updated_html_files:
                run_html_formatters(str(file))

        display_names = ", ".join(m.get("name") for m in django_models)
        self.stdout.write(self.style.SUCCESS(f"CRUD views generated for: {display_names}"))

    @classmethod
    def get_models_data(cls, app_label: str, excluded_fields: list[str], *, entry_point: bool) -> "list[DjangoModel]":
        models = apps.get_app_config(app_label).get_models()
        file_fields = ("ImageField", "FileField")
        dates_fields = ("DateField", "DateTimeField", "TimeField")

        def get_model_dict(model) -> "DjangoModel":
            name = model.__name__
            name_lower = name.lower()
            if entry_point:
                name_plural = app_label.lower()
            else:
                name_plural = model._meta.verbose_name_plural or f"{name}s"  # noqa

            verbose_name = model._meta.verbose_name  # noqa
            verbose_name_plural = model._meta.verbose_name_plural  # noqa

            def get_accessor(field) -> str:
                base_accessor = f"{name_lower}.{field.name}"
                if field.__class__.__name__ in file_fields:
                    return f"{{% if {base_accessor} %}} {{{{ {base_accessor}.url }}}} {{% endif %}}"
                else:
                    return "{{" + base_accessor + "}}"

            fields: dict[str, DjangoField] = {
                field.name: {
                    "verbose_name": field.verbose_name,
                    "editable": field.editable,
                    "class_name": field.__class__.__name__,
                    "accessor": get_accessor(field)
                }
                for field in model._meta.fields  # noqa
                if field.name not in excluded_fields
            }
            name_lower = name.lower()
            lookup_field = getattr(model, "lookup_field", "pk")
            return {
                "name": name,
                "name_lower": name_lower,
                "name_plural": name_plural,
                "lookup_field": lookup_field,
                "path_converter": "int" if lookup_field == "pk" else "str",
                "fields": fields,
                "obj_accessor": "{{" + name_lower + "}}",
                "verbose_name": verbose_name,
                "verbose_name_plural": verbose_name_plural,
                "has_file_field": any(f["class_name"] in file_fields for f in fields.values()),
                "has_editable_date_field": any(
                    f["class_name"] in dates_fields and f["editable"] for f in fields.values()
                ),
            }

        return [get_model_dict(model) for model in models]

    @simple_progress("Generating python code")
    def generate_python_code(
        self,
        app: AppConfig,
        blueprints: list[Path],
        contexts: list["BlueprintContext"],
    ) -> list[Path]:
        updated_files = []

        for blueprint in blueprints:
            file_content = blueprint.read_text()
            imports_template = extract_content_from(file_content, IMPORT_START_COMMENT, IMPORT_END_COMMENT)
            code_template = extract_content_from(file_content, CODE_START_COMMENT, CODE_END_COMMENT)
            # blueprints python files end in .py.dtl
            file_name_without_jinja = ".".join(blueprint.name.split(".")[:-1])
            file_to_write_to = Path(app.path) / file_name_without_jinja
            file_to_write_to.touch(exist_ok=True)

            imports_content, code_content = "", ""

            for context in contexts:
                imports_content += render_from_string(imports_template, context)
                code_content += render_from_string(code_template, context)

            file_to_write_to.write_text(imports_content + file_to_write_to.read_text() + code_content)
            updated_files.append(file_to_write_to)

        model_name = contexts[0]["model"]["name"] if len(contexts) == 1 else None
        if not self.no_admin:
            updated_files.append(self.register_models_in_admin(app=app, model_name=model_name))
        return updated_files

    @simple_progress("Generating urls")
    def generating_urls(
        self,
        app: AppConfig,
        django_models: list["DjangoModel"],
        *,
        entry_point: bool,
    ) -> list[Path]:
        urls_content = ""
        for django_model in django_models:
            model_name_lower = django_model["name_lower"]
            urlsafe_model_verbose_name_plural = django_model["verbose_name_plural"].lower().replace(" ", "-")
            view_name_prefix = "" if entry_point else f"{model_name_lower}_"
            list_view_name = "index" if entry_point else f"{model_name_lower}_list"
            prefix = "" if entry_point else f"{urlsafe_model_verbose_name_plural}/"
            urls_content += f"""
                path('{prefix}', views.{list_view_name}, name='{list_view_name}'),
                path('{prefix}new/', views.process_{view_name_prefix}form, name='{view_name_prefix}create'),
                path('{prefix}<{django_model['path_converter']}:{django_model['lookup_field']}>/', views.{view_name_prefix}detail, name='{view_name_prefix}detail'),
                path('{prefix}<{django_model['path_converter']}:{django_model['lookup_field']}>/edit/', views.process_{view_name_prefix}form, name='{view_name_prefix}update'),
                path('{prefix}<{django_model['path_converter']}:{django_model['lookup_field']}>/delete/', views.{view_name_prefix}delete, name='{view_name_prefix}delete'),
            """

        app_urls = Path(app.path) / "urls.py"
        updated_files = [app_urls]
        if app_urls.exists() and app_urls.read_text().strip() != "":
            urlpatterns = f"\nurlpatterns +=[{urls_content}]"
            app_urls.write_text(app_urls.read_text() + urlpatterns)
        else:
            app_urls.touch()
            app_urls.write_text(
                f"""
from django.urls import path
from . import views

app_name = "{app.label}"

urlpatterns = [
{urls_content}
]
        """
            )
            root_url = settings.ROOT_URLCONF
            root_url = root_url.strip().replace(".", "/")
            root_url_path = Path(f"{root_url}.py")
            module = parso.parse(root_url_path.read_text())
            new_path = parso.parse(f",\n    path('{app.label}/', include('{app.name}.urls', namespace='{app.label}'))")
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
                        root_url_path.write_text(new_content)
                        break
                except AttributeError:
                    continue
            updated_files.append(root_url_path)
        return updated_files

    @simple_progress("Generating html templates")
    def generate_html_templates(
        self,
        templates_dir: Path,
        blueprints: list[Path],
        contexts: list["BlueprintContext"],
        *,
        entry_point: bool,
    ) -> list[Path]:
        updated_files = []
        templates_dir.mkdir(exist_ok=True, parents=True)
        for blueprint in blueprints:
            for context in contexts:
                model_name_lower = context["model"]["name_lower"]
                if entry_point:
                    new_filename = "index.html" if blueprint.name == "list.html" else blueprint.name
                else:
                    new_filename = f"{model_name_lower}_{blueprint.name}"
                file_to_write_to = templates_dir / new_filename
                file_to_write_to.touch(exist_ok=True)
                views_content = render_from_string(blueprint.read_text(), context=context)

                file_to_write_to.write_text(views_content)
                updated_files.append(file_to_write_to)

        return updated_files

    def register_models_in_admin(self, app: AppConfig, model_name: str | None = None) -> Path:
        admin_file = Path(app.path) / "admin.py"

        # Skip further processing if model_name is not specified and file is non-empty
        if not model_name and admin_file.exists() and admin_file.stat().st_size > 0:
            self.stdout.write(self.style.WARNING("Skipping admin registration as the file is not empty."))
            return admin_file

        admin_file.touch(exist_ok=True)
        cmd_args = [app.label]
        if model_name:
            cmd_args.append(model_name)

        try:
            output = StringIO()
            call_command("admin_generator", *cmd_args, stdout=output)
        except CommandError as e:
            self.stdout.write(self.style.WARNING(f"Admin failed to generate: {e}"))
            return admin_file

        # the first line of the generated code set the encoding, it is useless for python 3
        admin_code = output.getvalue().split("\n", 1)[1]
        existing_code = admin_file.read_text()

        if model_name and model_name.title() in existing_code:
            self.stdout.write(self.style.WARNING(f"Model {model_name} is already registered."))
            return admin_file

        admin_file.write_text(existing_code + admin_code)

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


def build_blueprint_context(
    app_label: str,
    django_model: DjangoModel,
    *,
    entry_point: bool,
    login_required: bool,
    order_by: str | None = None,
) -> BlueprintContext:
    model_name_lower = django_model["name_lower"]
    view_name_prefix = "" if entry_point else f"{model_name_lower}_"
    list_view_name = "index" if entry_point else f"{model_name_lower}_list"
    detail_view_name = f"{view_name_prefix}detail"
    update_view_name = f"{view_name_prefix}update"
    delete_view_name = f"{view_name_prefix}delete"
    create_view_url = f"{{% url '{app_label}:{view_name_prefix}create' %}}"
    ordering = order_by or django_model["lookup_field"]
    project_name = settings.ROOT_URLCONF.rsplit(".", 1)[0]

    fields = django_model["fields"]
    field_names = list(fields.keys())

    table_headers = "".join(
        f"<th>{fields[f]['verbose_name']}</th>" for f in field_names
    )

    table_cells = ""
    for idx, f in enumerate(field_names):
        klass = fields[f]["class_name"]
        if idx == 0:
            cell = (
                f'<td><a class="font-medium hover:underline" href="'
                f'{{% url \'{app_label}:{detail_view_name}\' object.{django_model["lookup_field"]} %}}">'
                f'{{{{object.{f}}}}}</a></td>'
            )
        elif klass in ("BooleanField", "NullBooleanField"):
            cell = (
                f'<td class="text-center">'
                f'{{% if object.{f} %}}'
                f'{{% heroicon_solid "check-circle" size=19 class="text-green-500 mx-auto" %}}'
                f'{{% else %}}'
                f'{{% heroicon_solid "x-circle" size=19 class="text-red-500 mx-auto" %}}'
                f'{{% endif %}}'
                f'</td>'
            )
        elif klass in ("ImageField", "FileField"):
            cell = (
                f'<td>'
                f'{{% if object.{f} %}}'
                f'<a class="hover:underline" href="{{{{object.{f}.url}}}}">{{{{object.{f}.name}}}}</a>'
                f'{{% endif %}}'
                f'</td>'
            )
        else:
            cell = f'<td>{{{{object.{f}}}}}</td>'
        table_cells += cell

    actions_cell = (
        f'<td class="flex gap-3">'
        f'<a class="hover:text-blue-500" href="{{% url \'{app_label}:{detail_view_name}\' object.{django_model["lookup_field"]} %}}">{{% heroicon_outline "eye" size=18 %}}</a>'
        f'<a class="hover:text-blue-500" href="{{% url \'{app_label}:{update_view_name}\' object.{django_model["lookup_field"]} %}}">{{% heroicon_outline "pencil-square" size=18 %}}</a>'
        f'<form hx-boost="true" hx-target="closest tr" hx-push-url="false" '
        f'action="{{% url \'{app_label}:{delete_view_name}\' object.{django_model["lookup_field"]} %}}" class="cursor-pointer text-red-600 hover:text-red-500" '
        f'method="post" onsubmit="return confirm(\'Do you really want to delete this element?\');">'
        f'{{% csrf_token %}}'
        f'<button type="submit">{{% heroicon_outline "trash" size=18 %}}</button>'
        f'</form>'
        f'</td>'
    )

    return {
        "project_name": project_name,
        "app_label": app_label,
        "model": django_model,
        "fields_tuple": tuple(field_names),
        "editable_fields_tuple": tuple(
            key for key, value in fields.items() if value["editable"]
        ),
        "view_name_prefix": view_name_prefix,
        "list_view_name": list_view_name,
        "detail_view_name": detail_view_name,
        "delete_view_name": delete_view_name,
        "list_view_url": f"{{% url '{app_label}:{list_view_name}' %}}",
        "create_view_url": create_view_url,
        "detail_view_url": f"{{% url '{app_label}:{detail_view_name}' {model_name_lower}.{django_model['lookup_field']} %}}",
        "update_view_url": f"{{% url '{app_label}:{update_view_name}' {model_name_lower}.{django_model['lookup_field']} %}}",
        "delete_view_url": f"{{% url '{app_label}:{delete_view_name}' {model_name_lower}.{django_model['lookup_field']} %}}",
        "entry_point": entry_point,
        "login_required": login_required,
        "ordering": ordering,
        "pagination_block": (
            f'{{% if {model_name_lower}s_page.paginator.num_pages > 1 %}}'
            f'<c-pagination page={model_name_lower}s_page />'
            f'{{% endif %}}'
        ),
        "table_block": (
            f'{{% if {model_name_lower}s_page.object_list %}}'
            f'<div class="overflow-x-auto">'
            f'<table class="table">'
            f'<caption>A list of {django_model["verbose_name_plural"]}.</caption>'
            f'<thead><tr>{table_headers}</tr></thead>'
            f'<tbody>'
            f'{{% for object in {model_name_lower}s_page.object_list %}}'
            f'<tr>{table_cells}{actions_cell}</tr>'
            f'{{% endfor %}}'
            f'</tbody>'
            f'</table>'
            f'</div>'
            f'{{% else %}}'
            f'<p class="mt-8">There are no {django_model["verbose_name_plural"]}. <a class="hover:underline cursor-pointer" href="{create_view_url}">Create one now?</a> </p>'
            f'{{% endif %}}'
        ),
    }


def render_from_string(template_string: str, context: dict) -> str:
    return Template(template_string).render(Context(context))


def extract_content_from(text: str, start_comment: str, end_comment: str):
    start_index = text.find(start_comment) + len(start_comment)
    end_index = text.find(end_comment)
    return text[start_index:end_index]
