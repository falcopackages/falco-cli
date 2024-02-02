import subprocess
from pathlib import Path

import cappa
import pytest
from cappa.testing import CommandRunner
from falco.config import write_falco_config

views_functions = ["post_list", "post_detail", "post_update", "post_create"]
html_templates = [
    "post_list.html",
    "post_detail.html",
    "post_update.html",
    "post_create.html",
]
views_functions_entry_point = ["index", "detail", "update", "create"]
html_templates_point = [
    "index.html",
    "detail.html",
    "update.html",
    "create.html",
]
forms_attributes = ["PostForm", "Post", "title", "content"]
admin_attributes = ["PostAdmin", "Post", "title", "content"]


def create_pyproject_crud_config(**kwargs):
    pyproject_toml = Path("pyproject.toml")
    pyproject_toml.touch()
    write_falco_config(pyproject_path=pyproject_toml, crud=kwargs)


def healthy_django_project() -> bool:
    result = subprocess.run(
        ["python", "manage.py", "check"],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def fix_users_import():
    types = Path("core/types.py")
    types.write_text(types.read_text().replace("myproject.users", "django.contrib.auth"))


def install_crud_utils(runner):
    runner.invoke("install-crud-utils", "core")
    fix_users_import()


def test_crud(django_project, runner: CommandRunner, set_git_repo_to_clean):
    install_crud_utils(runner)
    runner.invoke("crud", "blog.post")
    assert healthy_django_project()
    app_dir = Path("blog")
    assert (app_dir / "urls.py").exists()
    # sourcery skip: no-loop-in-tests
    for a in forms_attributes:
        assert a in (app_dir / "forms.py").read_text()

    for a in admin_attributes:
        assert a in (app_dir / "admin.py").read_text()

    for f in views_functions:
        assert f in (app_dir / "views.py").read_text()
    for t in html_templates:
        assert (app_dir / "templates" / "blog" / f"{t}").exists()


def test_crud_login(django_project, runner: CommandRunner, set_git_repo_to_clean):
    install_crud_utils(runner)
    runner.invoke("crud", "blog.post", "--login-required")
    assert healthy_django_project()
    app_dir = Path("blog")
    assert (app_dir / "urls.py").exists()
    for a in forms_attributes:
        assert a in (app_dir / "forms.py").read_text()

    for a in admin_attributes:
        assert a in (app_dir / "admin.py").read_text()

    # sourcery skip: no-loop-in-tests
    for f in views_functions:
        assert f in (app_dir / "views.py").read_text()
    for t in html_templates:
        assert (app_dir / "templates" / "blog" / f"{t}").exists()


def test_crud_entry_point(django_project, runner: CommandRunner, set_git_repo_to_clean):
    install_crud_utils(runner)
    runner.invoke("crud", "blog.post", "--entry-point")
    assert healthy_django_project()
    app_dir = Path("blog")
    assert (app_dir / "urls.py").exists()
    for a in forms_attributes:
        assert a in (app_dir / "forms.py").read_text()

    for a in admin_attributes:
        assert a in (app_dir / "admin.py").read_text()
    # sourcery skip: no-loop-in-tests
    for f in views_functions_entry_point:
        assert f in (app_dir / "views.py").read_text()
    for t in html_templates_point:
        assert (app_dir / "templates" / "blog" / f"{t}").exists()


def test_crud_entry_point_login(django_project, runner: CommandRunner, set_git_repo_to_clean):
    install_crud_utils(runner)
    runner.invoke("crud", "blog.post", "--entry-point", "--login-required")
    assert healthy_django_project()
    app_dir = Path("blog")
    assert (app_dir / "urls.py").exists()
    for a in forms_attributes:
        assert a in (app_dir / "forms.py").read_text()

    for a in admin_attributes:
        assert a in (app_dir / "admin.py").read_text()
    # sourcery skip: no-loop-in-tests
    for f in views_functions_entry_point:
        assert f in (app_dir / "views.py").read_text()
    for t in html_templates_point:
        assert (app_dir / "templates" / "blog" / f"{t}").exists()


def test_crud_only_html(django_project, runner: CommandRunner, set_git_repo_to_clean):
    install_crud_utils(runner)
    runner.invoke("crud", "blog.post", "--only-html")
    assert healthy_django_project()
    app_dir = Path("blog")
    assert not (app_dir / "urls.py").exists()
    assert not (app_dir / "forms.py").exists()
    # sourcery skip: no-loop-in-tests
    for f in views_functions:
        assert f not in (app_dir / "views.py").read_text()
    for t in html_templates:
        assert (app_dir / "templates" / "blog" / f"{t}").exists()


def test_crud_only_python(django_project, runner: CommandRunner, set_git_repo_to_clean):
    install_crud_utils(runner)
    runner.invoke("crud", "blog.post", "--only-python")
    assert healthy_django_project()
    app_dir = Path("blog")
    assert (app_dir / "urls.py").exists()
    # sourcery skip: no-loop-in-tests
    for a in forms_attributes:
        assert a in (app_dir / "forms.py").read_text()

    for a in admin_attributes:
        assert a in (app_dir / "admin.py").read_text()
    # sourcery skip: no-loop-in-tests
    for f in views_functions:
        assert f in (app_dir / "views.py").read_text()
    for t in html_templates:
        assert not (app_dir / "templates" / "blog" / f"{t}").exists()


def test_crud_repo_not_clean(django_project, runner: CommandRunner):
    with pytest.raises(cappa.Exit):
        runner.invoke("crud", "blog.post")


def test_crud_exclude_field(django_project, runner: CommandRunner, set_git_repo_to_clean):
    install_crud_utils(runner)
    runner.invoke("crud", "blog.post", "-e=title")
    app_dir = Path("blog")
    # sourcery skip: no-loop-in-tests
    assert "title" not in (app_dir / "forms.py").read_text()
    assert "title" not in (app_dir / "views.py").read_text()
    assert "post.title" not in (app_dir / "templates/blog/post_list.html").read_text()
    forms_attributes_ = ["PostForm", "Post", "content"]
    for a in forms_attributes_:
        assert a in (app_dir / "forms.py").read_text()


def test_crud_login_required(django_project, runner: CommandRunner, set_git_repo_to_clean):
    install_crud_utils(runner)
    runner.invoke("crud", "blog.post", "--login-required")
    assert healthy_django_project()
    views = (Path("blog") / "views.py").read_text()
    assert "@login_required" in views
    assert "AuthenticatedHttpRequest" in views


def test_crud_config_pyproject_skip_git_check_set(django_project, runner: CommandRunner):
    create_pyproject_crud_config(skip_git_check=True)
    install_crud_utils(runner)
    runner.invoke("crud", "blog.post")
    assert healthy_django_project()
    views = (Path("blog") / "views.py").read_text()
    assert "post_list" in views


def test_crud_config_pyproject_login_required(django_project, runner: CommandRunner):
    create_pyproject_crud_config(skip_git_check=True, login_required=True)
    install_crud_utils(runner)
    runner.invoke("crud", "blog.post")
    assert healthy_django_project()
    views = (Path("blog") / "views.py").read_text()
    assert "@login_required" in views
    assert "AuthenticatedHttpRequest" in views


def test_crud_config_pyproject_blueprints(django_project, runner: CommandRunner):
    bp = django_project / "blueprints"
    bp.mkdir()
    html_file = bp / "dummy.html"
    html_file.touch()
    html_file.write_text("{{ model_name }}")
    create_pyproject_crud_config(blueprints=str(Path("blueprints")), skip_git_check=True)
    install_crud_utils(runner)
    runner.invoke("crud", "blog.post")
    views = (Path("blog") / "views.py").read_text()
    rendered_file = Path("blog") / "templates" / "blog" / "post_dummy.html"
    assert rendered_file.exists()
    assert "Post" in rendered_file.read_text()
    assert "Post" in views


def test_crud_always_migrate(django_project, runner: CommandRunner, set_git_repo_to_clean):
    create_pyproject_crud_config(always_migrate=True)
    settings = django_project / "myproject" / "settings.py"
    settings.write_text(settings.read_text() + "\n\n" + "INSTALLED_APPS += ['non_existent_app']\n")
    install_crud_utils(runner)
    with pytest.raises(cappa.Exit):
        runner.invoke("crud", "blog.post")
    assert "post_list" not in Path("blog/views.py").read_text()
    assert not healthy_django_project()
