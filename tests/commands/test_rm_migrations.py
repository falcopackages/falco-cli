import subprocess
from pathlib import Path

import cappa
import pytest
from cappa.testing import CommandRunner


def makemigaration():
    subprocess.run(["python", "manage.py", "makemigrations"], check=False)


def test_rm_migrations(django_project, runner: CommandRunner, set_git_repo_to_clean):
    apps_dir = Path()
    makemigaration()
    first_migration = apps_dir / "blog/migrations/0001_initial.py"
    assert first_migration.exists()
    runner.invoke("rm-migrations", ".")
    assert not first_migration.exists()


def test_rm_migrations_fake_apps_dir(django_project, runner: CommandRunner, set_git_repo_to_clean):
    apps_dir = Path()
    makemigaration()
    first_migration = apps_dir / "blog/migrations/0001_initial.py"
    assert first_migration.exists()
    runner.invoke("rm-migrations", "myproject")
    assert first_migration.exists()


def test_rm_migrations_not_clean_repo(django_project, runner: CommandRunner):
    with pytest.raises(cappa.Exit):
        runner.invoke("rm-migrations", ".")
