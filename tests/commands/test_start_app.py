from pathlib import Path

from cappa.testing import CommandRunner
from tests.commands.test_crud import healthy_django_project


def test_start_app(django_project, runner: CommandRunner):
    runner.invoke("start-app", "products")
    assert Path("myproject/products").exists()
    assert healthy_django_project()
