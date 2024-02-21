import pytest
from falco.commands.work import default_address
from falco.commands.work import default_server_cmd
from falco.commands.work import Work
from falco.config import write_falco_config


def test_env_resolution(tmp_path):
    assert Work().resolve_django_env()


def test_env_resolution_with_env(tmp_path):
    (tmp_path / ".env").write_text("FOO=BAR")
    assert "FOO" in Work().resolve_django_env()


def test_without_pyproject_file():
    assert Work().get_commands() == {"server": default_server_cmd.format(address=default_address)}


def test_with_pyproject_file(pyproject_toml):
    write_falco_config(pyproject_path=pyproject_toml, work={"qcluster": "python manage.py qcluster"})
    assert Work().get_commands() == {
        "server": default_server_cmd.format(address=default_address),
        "qcluster": "python manage.py qcluster",
    }


def test_override_server(pyproject_toml):
    work = {"server": "python manage.py runserver", "qcluster": "python manage.py qcluster"}
    write_falco_config(pyproject_path=pyproject_toml, work=work)
    assert Work().get_commands() == work


@pytest.mark.parametrize("address", ["8000", "localhost:8000", "8001", "127.0.0.1"])
def test_override_server_through_arg(address):
    assert Work(address=address).get_commands() == {"server": default_server_cmd.format(address=address)}
