import subprocess

from cappa.testing import CommandRunner
from falco.utils import run_in_shell


def makemigrations():
    subprocess.run(["python", "manage.py", "makemigrations"], check=False)


def migrate():
    subprocess.run(["python", "manage.py", "migrate"], check=False)


def add_settings(django_project_dir):
    settings_file = django_project_dir / "myproject" / "settings.py"
    settings_content = settings_file.read_text()
    settings_file.write_text(
        settings_content + "\n" + "SUPERUSER_USERNAME = 'admin'\n" + "SUPERUSER_PASSWORD = 'admin'"
    )


def is_superuser_created():
    return run_in_shell(
        "from django.contrib.auth.models import User;"
        "print(User.objects.filter(is_superuser=True, username='admin').exists())"
    )


def test_setup_admin(django_project, runner: CommandRunner):
    add_settings(django_project)
    makemigrations()
    migrate()
    assert not is_superuser_created()
    runner.invoke("setup-admin")
    assert is_superuser_created()
