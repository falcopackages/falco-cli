from pathlib import Path
from typing import Annotated

import cappa
from falco.config import FalcoConfig
from falco.config import read_falco_config
from falco.config import write_falco_config
from falco.utils import get_project_name
from falco.utils import get_pyproject_file
from falco.utils import simple_progress
from rich import print as rich_print

from .utils import extract_python_file_templates
from .utils import get_crud_blueprints_path
from .utils import render_to_string
from .utils import run_python_formatters


@cappa.command(help="Install utils necessary for CRUD views.", name="install-crud-utils")
class InstallCrudUtils:
    output_dir: Annotated[
        Path | None,
        cappa.Arg(default=None, help="The folder in which to install the crud utils."),
    ] = None

    def __call__(self, project_name: Annotated[str, cappa.Dep(get_project_name)]):
        try:
            pyproject_path = get_pyproject_file()
            falco_config = read_falco_config(pyproject_path)
        except cappa.Exit:
            falco_config = {}
            pyproject_path = None

        output_dir = self.install(project_name=project_name, falco_config=falco_config)
        if pyproject_path:
            write_falco_config(pyproject_path=pyproject_path, crud={"utils_path": str(output_dir)})

        rich_print(f"[green]CRUD Utils installed successfully to {output_dir}.")

    def install(self, project_name: str, falco_config: FalcoConfig) -> Path:
        output_dir = self.output_dir or self.get_install_path(project_name=project_name, falco_config=falco_config)[0]

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

        for file in generated_files:
            run_python_formatters(str(file))

        return output_dir

    @classmethod
    def get_install_path(cls, project_name: str, falco_config: FalcoConfig) -> tuple[Path, bool]:
        if _import_path := falco_config.get("crud", {}).get("utils_path"):
            return Path(_import_path), True
        return Path(f"{project_name}/core"), False
