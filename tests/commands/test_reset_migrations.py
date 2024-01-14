import subprocess

from cappa.testing import CommandRunner
from falco.utils import run_in_shell


def makemigrations():
    subprocess.run(["python", "manage.py", "makemigrations"], check=False)


def migrate():
    subprocess.run(["python", "manage.py", "migrate"], check=False)


def change_model_attribute(django_project_dir):
    models_file = django_project_dir / "blog" / "models.py"
    models_file_content = models_file.read_text()
    models_file.write_text(
        models_file_content + "\n" + "    new_attribute = models.CharField(max_length=200, default='v')\n"
    )


def insert_a_post(django_project_dir):
    run_in_shell(
        "from blog.models import Post; Post.objects.create(title='t', content='c')",
        eval_result=False,
    )


def count_nbr_of_posts(django_project_dir):
    return run_in_shell("from blog.models import Post; print(Post.objects.all().count())")


def count_migrations(django_project_dir):
    migrations_folder = django_project_dir / "blog" / "migrations"
    return len([file for file in migrations_folder.iterdir() if file.name.startswith("000")])


def test_reset_migrations(django_project, runner: CommandRunner, set_git_repo_to_clean):
    makemigrations()
    migrate()

    insert_a_post(django_project)
    assert count_nbr_of_posts(django_project) == 1
    assert count_migrations(django_project) == 1

    change_model_attribute(django_project)
    makemigrations()
    migrate()

    assert count_migrations(django_project) == 2
    runner.invoke("reset-migrations", ".")
    assert count_migrations(django_project) == 1
    assert count_nbr_of_posts(django_project) == 1
