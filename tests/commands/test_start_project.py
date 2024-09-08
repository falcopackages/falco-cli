from pathlib import Path

import pytest
from cappa.testing import CommandRunner
from falco_cli.config import read_falco_config


def all_files_are_correctly_generated(project_name, project_dir: Path) -> bool:
    required_files = [
        "pyproject.toml",
        "README.md",
        ".gitignore",
        ".github",
        "deploy",
        "tests",
        "manage.py",
        ".env.template",
        "docs",
        "docs/conf.py",
        f"{project_name}/settings.py",
        f"{project_name}/urls.py",
        f"{project_name}/wsgi.py",
    ]
    return all((project_dir / file).exists() for file in required_files)


@pytest.mark.parametrize(
    "blueprint_path",
    [
        Path("blueprints/tailwind").resolve(strict=True),
        Path("blueprints/bootstrap").resolve(strict=True),
    ],
)
def test_start_project(blueprint_path, runner: CommandRunner):
    runner.invoke(
        "start-project",
        "dotfm",
        "--skip-new-version-check",
        "--blueprint",
        str(blueprint_path),
    )
    assert Path("dotfm").exists()
    config = read_falco_config(Path("dotfm/pyproject.toml"))
    config_keys = config.keys()
    assert "blueprint" in config_keys
    assert "revision" in config_keys
    assert "work" in config_keys

    assert all_files_are_correctly_generated("dotfm", project_dir=Path("dotfm"))


# def test_start_project_alias_name(runner: CommandRunner):
#     runner.invoke(
#         "start-project",
#         "dotfm",
#         "--skip-new-version-check",
#         "--blueprint",
#         "tailwind",
#     )
#     assert Path("dotfm").exists()
#     config = read_falco_config(Path("dotfm/pyproject.toml"))
#     config_keys = config.keys()
#     assert "blueprint" in config_keys
#     assert "revision" in config_keys
#     assert "work" in config_keys
#     assert len(config["revision"]) > 10
#
#     assert all_files_are_correctly_generated("dotfm", project_dir=Path("dotfm"))


@pytest.mark.parametrize(
    "blueprint_path",
    [
        Path("blueprints/tailwind").resolve(strict=True),
        Path("blueprints/bootstrap").resolve(strict=True),
    ],
)
def test_start_project_in_directory(blueprint_path, runner: CommandRunner, tmp_path):
    runner.invoke(
        "start-project",
        "dotfm",
        "builds",
        "--skip-new-version-check",
        "--blueprint",
        str(blueprint_path),
    )
    project_dir = tmp_path / "builds" / "dotfm"
    assert project_dir.exists()
    assert all_files_are_correctly_generated("dotfm", project_dir=project_dir)


@pytest.mark.parametrize(
    "blueprint_path",
    [
        Path("blueprints/tailwind").resolve(strict=True),
        Path("blueprints/bootstrap").resolve(strict=True),
    ],
)
def test_start_project_in_directory_with_root(blueprint_path, runner: CommandRunner, tmp_path):
    runner.invoke(
        "start-project",
        "dotfm",
        "builds/special_project",
        "--root",
        "--skip-new-version-check",
        "--blueprint",
        str(blueprint_path),
    )
    project_dir = tmp_path / "builds/special_project"
    assert project_dir.exists()
    assert all_files_are_correctly_generated("dotfm", project_dir=project_dir)


@pytest.mark.parametrize(
    "blueprint_path",
    [
        Path("blueprints/tailwind").resolve(strict=True),
        Path("blueprints/bootstrap").resolve(strict=True),
    ],
)
def test_user_name_and_email(blueprint_path, runner: CommandRunner, git_user_infos):
    name, email = git_user_infos
    runner.invoke(
        "start-project",
        "dotfm",
        "--skip-new-version-check",
        "--blueprint",
        str(blueprint_path),
    )
    pyproject_content = (Path("dotfm") / "pyproject.toml").read_text()
    assert name in pyproject_content
    assert email in pyproject_content


# def test_use_local_copy(runner: CommandRunner):
#     runner.invoke(
#         "start-project", "dotfm_cache", "--skip-new-version-check"
#     )  # to make sure the blueprint is downloaded a least once
#     with mock.patch("socket.socket", side_effect=OSError("Network access is cut off")):
#         runner.invoke("start-project", "dotfm", "--skip-new-version-check", "--local")
#     assert Path("dotfm").exists()
#     assert all_files_are_correctly_generated("dotfm", project_dir=Path("dotfm"))
