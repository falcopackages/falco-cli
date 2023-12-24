import subprocess
from pathlib import Path

import cappa
import pytest
from cappa.testing import CommandRunner


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


def healthy_django_project() -> bool:
    result = subprocess.run(
        ["python", "manage.py", "check"],
        check=False,
        capture_output=True,
        text=True,
    )
    print(result.stderr)
    return result.returncode == 0


def register_project_urls():
    urls_file = Path("myproject/urls.py")
    urls_file.write_text(
        "from django.urls import include\n\n"
        + urls_file.read_text()
        + "\n\nurlpatterns += [path('blog/', include('blog.urls'))]",
    )


def test_crud(django_project, runner: CommandRunner, set_git_repo_to_clean):
    runner.invoke("crud", "blog.post")
    runner.invoke("install-crud-utils", ".")
    register_project_urls()
    assert healthy_django_project()
    app_dir = Path("blog")
    assert (app_dir / "urls.py").exists()
    for a in forms_attributes:
        assert a in (app_dir / "forms.py").read_text()

    # sourcery skip: no-loop-in-tests
    for f in views_functions:
        assert f in (app_dir / "views.py").read_text()
    for t in html_templates:
        assert (app_dir / "templates" / "blog" / f"{t}").exists()


def test_crud_entry_point(django_project, runner: CommandRunner, set_git_repo_to_clean):
    runner.invoke("crud", "blog.post", "--entry-point")
    runner.invoke("install-crud-utils", ".")
    register_project_urls()
    assert healthy_django_project()
    app_dir = Path("blog")
    assert (app_dir / "urls.py").exists()
    for a in forms_attributes:
        assert a in (app_dir / "forms.py").read_text()
    # sourcery skip: no-loop-in-tests
    for f in views_functions_entry_point:
        assert f in (app_dir / "views.py").read_text()
    for t in html_templates_point:
        assert (app_dir / "templates" / "blog" / f"{t}").exists()


def test_crud_only_html(django_project, runner: CommandRunner, set_git_repo_to_clean):
    runner.invoke("crud", "blog.post", "--only-html")
    runner.invoke("install-crud-utils", ".")
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
    runner.invoke("crud", "blog.post", "--only-python")
    runner.invoke("install-crud-utils", ".")
    register_project_urls()
    assert healthy_django_project()
    app_dir = Path("blog")
    assert (app_dir / "urls.py").exists()
    # sourcery skip: no-loop-in-tests
    for a in forms_attributes:
        assert a in (app_dir / "forms.py").read_text()
    # sourcery skip: no-loop-in-tests
    for f in views_functions:
        assert f in (app_dir / "views.py").read_text()
    for t in html_templates:
        assert not (app_dir / "templates" / "blog" / f"{t}").exists()


def test_crud_repo_not_clean(django_project, runner: CommandRunner):
    with pytest.raises(cappa.Exit):
        runner.invoke("crud", "blog.post")


def test_crud_exclude_field(django_project, runner: CommandRunner, set_git_repo_to_clean):
    runner.invoke("crud", "blog.post", "--only-python", "-e=title")
    runner.invoke("install-crud-utils", ".")
    app_dir = Path("blog")
    # sourcery skip: no-loop-in-tests
    assert "title" not in (app_dir / "forms.py").read_text()
    forms_attributes_ = ["PostForm", "Post", "content"]
    for a in forms_attributes_:
        assert a in (app_dir / "forms.py").read_text()
