from pathlib import Path
from typing import Annotated

import cappa
from falco.utils import get_crud_blueprints_path
from falco.utils import get_project_name
from falco.utils import simple_progress
from rich import print as rich_print

from .model_crud import extract_python_file_templates
from .model_crud import run_python_formatters


@cappa.command(help="Install utils necessary for CRUD views.", name="install-crud-utils")
class InstallCrudUtils:
    apps_dir: Annotated[
        Path | None,
        cappa.Arg(default=None, help="The path to your django apps directory."),
    ]

    def __call__(self, project_name: Annotated[str, cappa.Dep(get_project_name)]):
        if not self.apps_dir:
            self.apps_dir = Path() / project_name

        output_dir = self.apps_dir / "core"
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "__init__.py").touch(exist_ok=True)

        generated_files = []
        crud_blueprint_path = get_crud_blueprints_path()

        with simple_progress("Installing crud utils"):
            for file in ["utils.py", "types.py"]:
                file_path = crud_blueprint_path / file
                imports_template, code_template = extract_python_file_templates(file_path.read_text())
                output_file = output_dir / file
                output_file.touch(exist_ok=True)
                output_file.write_text(imports_template + code_template + output_file.read_text())
                generated_files.append(output_file)

                # in case the types already include the HttpRequest import from django, it might class with the
                # types imports
                if file == "types.py":
                    content = output_file.read_text()
                    # remove the line with the exact text "from django.http import HttpRequest"
                    content = content.replace("from django.http import HttpRequest\n", "")
                    output_file.write_text(content.format(project_name=project_name))

        for file in generated_files:
            run_python_formatters(str(file))

        rich_print(f"[green]CRUD Utils installed successfully to {output_dir}.")
