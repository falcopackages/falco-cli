from pathlib import Path

from cappa.testing import CommandRunner
from falco.utils import get_falco_blueprints_path


def generated_project_files(project_name) -> list[str]:
    project_blueprint = get_falco_blueprints_path() / "project_name"
    result = []
    for file in project_blueprint.iterdir():
        if "project_name" in file.name:
            result.append(file.name.replace("project_name", project_name))
        else:
            result.append(file.name)
    return result


def test_start_project(runner: CommandRunner):
    runner.invoke("start-project", "dotfm", "--skip-new-version-check")
    assert Path("dotfm").exists()
    # sourcery skip: no-loop-in-tests
    project_files = [file.name for file in Path("dotfm").iterdir()]
    for file_name in generated_project_files("dotfm"):
        assert file_name in project_files


def test_user_name_and_email(runner: CommandRunner, git_user_infos):
    name, email = git_user_infos
    runner.invoke("start-project", "dotfm", "--skip-new-version-check")
    pyproject_content = (Path("dotfm") / "pyproject.toml").read_text()
    assert name in pyproject_content
    assert email in pyproject_content
