from pathlib import Path
from typing import Annotated

import cappa
from falco.utils import get_project_name
from falco.utils import simple_progress
from rich import print as rich_print

from .model_crud import extract_python_file_templates
from .model_crud import get_crud_blueprints_path
from .model_crud import render_to_string
from .model_crud import run_python_formatters


@cappa.command(help="Install utils necessary for CRUD views.", name="install-crud-utils")
class InstallCrudUtils:
    output_dir: Annotated[
        Path | None,
        cappa.Arg(default=None, help="The folder in which to install the crud utils."),
    ]

    def __call__(self, project_name: Annotated[str, cappa.Dep(get_project_name)]):
        output_dir = Path() / project_name / "core" if not self.output_dir else self.output_dir

        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "__init__.py").touch(exist_ok=True)

        generated_files = []

        context = {"project_name": project_name}
        with simple_progress("Installing crud utils"):
            for file_path in (get_crud_blueprints_path() / "utils").iterdir():
                imports_template, code_template = extract_python_file_templates(file_path.read_text())
                filename = ".".join(file_path.name.split(".")[:-1])
                output_file = output_dir / filename
                output_file.touch(exist_ok=True)
                output_file.write_text(
                    render_to_string(imports_template, context)
                    + render_to_string(code_template, context)
                    + output_file.read_text()
                )
                generated_files.append(output_file)

                # in case the types already include the HttpRequest import from django, it might class with the
                # types imports
                if file_path.name == "types.py.jinja":
                    content = output_file.read_text()
                    # remove the line with the exact text "from django.http import HttpRequest"
                    content = content.replace("from django.http import HttpRequest\n", "")

        for file in generated_files:
            run_python_formatters(str(file))

        rich_print(f"[green]CRUD Utils installed successfully to {output_dir}.")
