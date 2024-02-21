from pathlib import Path
from unittest.mock import patch

import pytest
from cappa.testing import CommandRunner
from falco.commands.htmx import Htmx
from falco.config import read_falco_config
from falco.config import write_falco_config


@pytest.fixture(autouse=True)
def mock_latest_tag_getter():
    def _get_latest_tag():
        return "1.9.10"

    with patch("falco.commands.htmx.get_latest_tag", new=_get_latest_tag):
        yield


def test_htmx_download(runner: CommandRunner):
    runner.invoke("htmx")
    assert Path("htmx.min.js").exists()


def test_htmx_download_with_version(runner: CommandRunner):
    runner.invoke("htmx", "latest")
    assert Path("htmx.min.js").exists()


def test_htmx_download_with_specific_version(runner: CommandRunner):
    runner.invoke("htmx", "1.8.0")
    assert Path("htmx.min.js").exists()


def test_htmx_download_to_output_dir(runner: CommandRunner):
    output = Path("htmx/vendors")
    runner.invoke("htmx", "-o", str(output.resolve()))
    assert (output / "htmx.min.js").exists()


def test_htmx_download_to_output_file(runner: CommandRunner):
    output = Path("htmx/vendors/htmx.js")
    runner.invoke("htmx", "-o", str(output.resolve()))
    assert output.exists()


def test_htmx_with_pyproject_toml(runner: CommandRunner):
    pyproject_toml = Path("pyproject.toml")
    pyproject_toml.touch()
    write_falco_config(pyproject_path=pyproject_toml)
    runner.invoke("htmx")
    assert Path("htmx.min.js").exists()
    filepath, version = Htmx.read_from_config(read_falco_config(pyproject_toml))
    assert filepath == Path("htmx.min.js")


def test_htmx_with_pyproject_toml_custom_folder(runner: CommandRunner):
    pyproject_toml = Path("pyproject.toml")
    pyproject_toml.touch()
    write_falco_config(pyproject_path=pyproject_toml)
    runner.invoke("htmx", "-o", "static/htmx")
    output = Path("static/htmx/htmx.min.js")
    assert output.exists()
    filepath, version = Htmx.read_from_config(read_falco_config(pyproject_toml))
    assert filepath == output


def test_htmx_with_pyproject_toml_custom_file(runner: CommandRunner):
    pyproject_toml = Path("pyproject.toml")
    pyproject_toml.touch()
    write_falco_config(pyproject_path=pyproject_toml)
    runner.invoke("htmx", "-o", "static/htmx/htmx.js")
    output = Path("static/htmx/htmx.js")
    assert output.exists()
    filepath, version = Htmx.read_from_config(read_falco_config(pyproject_toml))
    assert filepath == output


def test_htmx_with_pyproject_toml_custom_file_existing_config(runner: CommandRunner):
    pyproject_toml = Path("pyproject.toml")
    pyproject_toml.touch()
    write_falco_config(pyproject_path=pyproject_toml, htmx="config/htmx/htmx.js")
    existing_path = Path("config/htmx/htmx.js")
    runner.invoke("htmx")
    filepath, _ = Htmx.read_from_config(read_falco_config(pyproject_toml))
    assert filepath == existing_path
    assert existing_path.exists()
