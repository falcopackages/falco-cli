from pathlib import Path
from typing import Annotated

import cappa
from falco.utils import get_current_dir_as_project_name
from falco.utils import get_falco_blueprints_path
from falco.utils import simple_progress
from rich import print as rich_print

from .model_crud import extract_python_file_templates
from .model_crud import run_python_formatters


UTILS_FILE = get_falco_blueprints_path() / "crud" / "utils.py"
DEFAULT_INSTALL_PATH = "core/utils.py"


@cappa.command(help="Install utils necessary for CRUD views.", name="install-crud-utils")
class InstallCrudUtils:
    apps_dir: Annotated[
        Path | None,
        cappa.Arg(default=None, help="The path to your django apps directory."),
    ]
    output: Annotated[
        Path,
        cappa.Arg(
            default=Path(DEFAULT_INSTALL_PATH),
            help="The directory to write the utils file to.",
            short="-o",
            long="--output",
        ),
    ]

    def __call__(self, project_name: Annotated[str, cappa.Dep(get_current_dir_as_project_name)]):
        if not self.apps_dir:
            self.apps_dir = Path() / project_name

        output = self.apps_dir / self.output

        with simple_progress("Installing crud utils"):
            imports_template, code_template = extract_python_file_templates(UTILS_FILE.read_text())
            output_file = output if output.name.endswith(".py") else output / "utils.py"
            output_file.parent.mkdir(parents=True, exist_ok=True)
            (output_file.parent / "__init__.py").touch(exist_ok=True)
            output_file.touch(exist_ok=True)
            output_file.write_text(imports_template + output_file.read_text() + code_template)
        run_python_formatters(str(output_file))
        rich_print(f"[green]CRUD Utils installed successfully to {output_file}.")
