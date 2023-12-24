import os
import subprocess

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
    subprocess.run(["django-admin", "startproject", "myproject", str(project_dir)], check=True)
    os.chdir(project_dir)

    # Create a new Django app
    subprocess.run(["python", "manage.py", "startapp", "myapp"], check=True)

    # Create a basic model in the app
    model_code = """
from django.db import models

class MyModel(models.Model):
    field1 = models.CharField(max_length=200)
    field2 = models.IntegerField()
    """
    (project_dir / "myapp" / "models.py").write_text(model_code)

    yield project_dir
    os.chdir(tmp_path)
