from pathlib import Path

from cappa.testing import CommandRunner
from falco.config import write_falco_config


def test_install_crud_utils(runner: CommandRunner, pyproject_toml):
    runner.invoke("install-crud-utils", ".")
    assert Path("utils.py").exists()
    assert Path("types.py").exists()
    assert Path("__init__.py").exists()


def test_install_crud_utils_to_output_dir(runner: CommandRunner, pyproject_toml):
    output = Path("myapp")
    runner.invoke("install-crud-utils", str(output.resolve()))
    assert (output / "utils.py").exists()
    assert (output / "types.py").exists()
    assert (output / "__init__.py").exists()


def test_install_crud_utils_to_existing_config(runner: CommandRunner, pyproject_toml):
    pyproject_toml = Path("pyproject.toml")
    write_falco_config(pyproject_path=pyproject_toml, crud={"utils_path": "myproject/special_utils_dir"})
    output = Path("myproject/special_utils_dir")
    runner.invoke("install-crud-utils")
    assert (output / "utils.py").exists()
    assert (output / "types.py").exists()
    assert (output / "__init__.py").exists()
