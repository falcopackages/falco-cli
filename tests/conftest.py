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
    """
    (project_dir / "blog" / "models.py").write_text(model_code)

    # Register the app in the project's settings
    settings_file = project_dir / "myproject" / "settings.py"
    settings_content = settings_file.read_text()
    settings_file.write_text(settings_content + "\n" + "INSTALLED_APPS += ['blog']\n")

    yield project_dir
    os.chdir(tmp_path)


@pytest.fixture
def set_git_repo_to_clean():
    # Define the mock function
    def mock_run(args, **kwargs):
        if args == ["git", "status", "--porcelain"]:
            mock = MagicMock()
            mock.returncode = 0
            mock.stdout = ""
            return mock
        else:
            # Call the original subprocess.run function
            return original_run(args, **kwargs)

    # Save the original subprocess.run function
    original_run = subprocess.run

    # Use patch to replace subprocess.run with the mock function
    with patch("subprocess.run", side_effect=mock_run):
        yield
