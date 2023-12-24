from pathlib import Path

from cappa.testing import CommandRunner
from falco.commands.install_crud_utils import DEFAULT_INSTALL_PATH


def test_install_crud_utils(runner: CommandRunner):
    runner.invoke("install-crud-utils")
    assert Path(DEFAULT_INSTALL_PATH).exists()


def test_install_crud_utils_to_output_dir(runner: CommandRunner):
    output = Path("core")
    runner.invoke("install-crud-utils", "-o", str(output.resolve()))
    assert (output / "utils.py").exists


def test_install_crud_utils_to_output_file(runner: CommandRunner):
    output = Path("core/utils.py")
    runner.invoke("install-crud-utils", "-o", str(output.resolve()))
    assert output.exists()
