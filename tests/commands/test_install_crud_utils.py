from pathlib import Path

from cappa.testing import CommandRunner
from falco.commands.install_crud_utils import DEFAULT_INSTALL_PATH


def test_install_crud_utils(runner: CommandRunner):
    runner.invoke("install-crud-utils", ".")
    assert Path(DEFAULT_INSTALL_PATH).exists()
    assert Path("core/__init__.py").exists()


def test_install_crud_utils_to_output_dir(runner: CommandRunner):
    output = Path("core")
    runner.invoke("install-crud-utils", ".", "-o", str(output.resolve()))
    assert (output / "utils.py").exists


def test_install_crud_utils_to_output_file(runner: CommandRunner):
    output = Path("core/utils.py")
    runner.invoke("install-crud-utils", ".", "-o", str(output.resolve()))
    assert output.exists()


def test_install_crud_utils_in_specific_apps_dir(runner: CommandRunner):
    apps_dir = Path("apps")
    runner.invoke("install-crud-utils", str(apps_dir.resolve()))
    assert (apps_dir / DEFAULT_INSTALL_PATH).exists()
    assert (apps_dir / "core/__init__.py").exists()


def test_install_crud_utils_in_specific_apps_dir_and_output(runner: CommandRunner):
    apps_dir = Path("apps")
    output = "core"
    dest_folder = apps_dir / output
    runner.invoke("install-crud-utils", str(apps_dir.resolve()), "-o", output)
    assert (dest_folder / "utils.py").exists()
    assert (dest_folder / "__init__.py").exists()
