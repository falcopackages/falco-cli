from pathlib import Path

from cappa.testing import CommandRunner


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
