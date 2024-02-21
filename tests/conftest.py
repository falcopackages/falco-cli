import os
import subprocess
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from cappa.testing import CommandRunner
from falco.__main__ import Falco


@pytest.fixture(autouse=True)
def change_test_dir(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)


@pytest.fixture
def runner():
    return CommandRunner(Falco)


@pytest.fixture
def django_project(tmp_path):
    project_dir = tmp_path / "myproject"
    subprocess.run(["django-admin", "startproject", "myproject"], check=True)
    os.chdir(project_dir)

    # Create a new Django app
    subprocess.run(["python", "manage.py", "startapp", "blog"], check=True)

    # Create a basic model in the app
    model_code = """
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    """
    (project_dir / "blog" / "models.py").write_text(model_code)

    # Register the app in the project's settings
    settings_file = project_dir / "myproject" / "settings.py"
    settings_content = settings_file.read_text()
    settings_file.write_text(settings_content + "\n" + "INSTALLED_APPS += ['blog', 'django_extensions']\n")

    # create a pyproject.toml
    (project_dir / "pyproject.toml").write_text(
        """
[project]
name = "myproject"
version = "0.1.0"
"""
    )

    yield project_dir
    os.chdir(tmp_path)


@pytest.fixture
def set_git_repo_to_clean():
    def mock_run(args, **kwargs):
        if args == ["git", "status", "--porcelain"]:
            mock = MagicMock()
            mock.returncode = 0
            mock.stdout = ""
            return mock
        return original_run(args, **kwargs)

    original_run = subprocess.run

    with patch("subprocess.run", side_effect=mock_run):
        yield


@pytest.fixture
def pyproject_toml(tmp_path):
    pyproject_toml = tmp_path / "pyproject.toml"
    pyproject_toml.write_text(
        """
        [project]
        name = "myproject"
        version = "0.1.0"
        """
    )
    yield pyproject_toml
    pyproject_toml.unlink()


@pytest.fixture
def git_user_infos():
    name = "John Doe"
    email = "johndoe@example.com"

    def mock_run(args, **kwargs):
        if args == ["git", "config", "--global", "--get", "user.name"]:
            mock = MagicMock()
            mock.returncode = 0
            mock.stdout = name
            return mock
        if args == ["git", "config", "--global", "--get", "user.email"]:
            mock = MagicMock()
            mock.returncode = 0
            mock.stdout = email
            return mock

        return original_run(args, **kwargs)

    original_run = subprocess.run

    with patch("subprocess.run", side_effect=mock_run):
        yield name, email
