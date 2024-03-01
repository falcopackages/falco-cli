import io
import os
from pathlib import Path
from unittest.mock import patch

import tomlkit
from cappa.testing import CommandRunner


def test_sync_dotenv(runner: CommandRunner, pyproject_toml):
    runner.invoke("sync-dotenv")
    env_file = Path(".env")
    env_template_file = Path(".env.template")
    assert env_file.exists()
    assert env_template_file.exists()
    assert "DEBUG=True" in env_file.read_text()
    assert "DEBUG=" in env_template_file.read_text()


def test_sync_dotenv_update_files(runner: CommandRunner, pyproject_toml):
    env_file = Path(".env")
    env_template_file = Path(".env.template")
    env_file.write_text("ANOTHER_SPECIAL_ENV=True")
    env_template_file.write_text("SPECIAL_ENV=")
    runner.invoke("sync-dotenv")
    assert "SPECIAL_ENV=" in env_file.read_text()
    assert "ANOTHER_SPECIAL_ENV=" in env_template_file.read_text()


def test_sync_dotenv_priority(runner: CommandRunner, pyproject_toml):
    env_file = Path(".env")
    env_template_file = Path(".env.template")
    env_file.write_text("SPECIAL_ENV=True")
    env_template_file.write_text("SPECIAL_ENV=")
    runner.invoke("sync-dotenv")
    assert "SPECIAL_ENV=True" in env_file.read_text()


def test_print_value(runner: CommandRunner, pyproject_toml):
    env_template_file = Path(".env.template")
    env_template_file.write_text("SPECIAL_ENV=")
    with patch("sys.stdout", new=io.StringIO()) as fake_stdout:
        runner.invoke("sync-dotenv", "-p")
        stdout = fake_stdout.getvalue()
        assert not Path(".env").exists()
        assert "SPECIAL_ENV=" in stdout


def test_prod_config(runner: CommandRunner, pyproject_toml):
    os.environ["DEBUG"] = "False"
    pyproject = tomlkit.parse(pyproject_toml.read_text())
    pyproject["project"]["authors"] = [{"email": "tobidegnon@proton.me", "name": "Tobi DEGNON"}]
    pyproject_toml.write_text(tomlkit.dumps(pyproject))
    runner.invoke("sync-dotenv")
    assert "DEBUG=False" in Path(".env").read_text()
    assert "DJANGO_SUPERUSER_EMAIL=tobidegnon@proton.me" in Path(".env").read_text()
    assert "SECRET_KEY=" in Path(".env").read_text()


# TODO: test fill missing and duplicate
