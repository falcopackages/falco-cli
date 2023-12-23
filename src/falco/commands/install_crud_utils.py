from pathlib import Path
from typing import Annotated

import cappa
from falco.utils import get_falco_blueprints_path
from falco.utils import simple_progress
from rich import print as rich_print

from .model_crud import extract_python_file_templates
from .model_crud import run_python_formatters


UTILS_FILE = get_falco_blueprints_path() / "crud" / "utils.py"


@cappa.command(help="Install utils necessary for CRUD views.", name="install-crud-utils")
class InstallCrudUtils:
    output: Annotated[
        Path,
        cappa.Arg(
            default=Path("core/utils.py"),
            help="The directory to write the utils file to.",
            short="-o",
            long="--output",
        ),
    ]

    def __call__(self):
        with simple_progress("Installing crud utils"):
            imports_template, code_template = extract_python_file_templates(UTILS_FILE.read_text())
            output_file = self.output if self.output.name.endswith(".py") else self.output / "utils.py"
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(imports_template + self.output.read_text() + code_template)
        run_python_formatters(str(output_file))
        rich_print("[green]CRUD Utils installed successfully.")
