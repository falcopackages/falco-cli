from pathlib import Path

from cappa.testing import CommandRunner
from falco.config import read_falco_config


def generated_project_files(project_name) -> list[str]:
    return [
        project_name,
        "pyproject.toml",
        "README.md",
        ".gitignore",
        "config",
        ".github",
        "deploy",
        "tests",
        "manage.py",
        ".env.template",
    ]


blueprint_path = Path("blueprints/falco_blueprint_basic").resolve(strict=True)


def test_start_project(runner: CommandRunner):
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
    assert "utils_path" in config.get("crud")
    assert "blueprint" in config_keys
    assert "revision" in config_keys
    assert "work" in config_keys

    # sourcery skip: no-loop-in-tests
    project_files = [file.name for file in Path("dotfm").iterdir()]
    for file_name in generated_project_files("dotfm"):
        assert file_name in project_files


def test_start_project_alias_name(runner: CommandRunner):
    runner.invoke(
        "start-project",
        "dotfm",
        "--skip-new-version-check",
        "--blueprint",
        "tailwind",
    )
    assert Path("dotfm").exists()
    config = read_falco_config(Path("dotfm/pyproject.toml"))
    config_keys = config.keys()
    assert "utils_path" in config.get("crud")
    assert "blueprint" in config_keys
    assert "revision" in config_keys
    assert "work" in config_keys
    assert len(config["revision"]) > 10

    # sourcery skip: no-loop-in-tests
    project_files = [file.name for file in Path("dotfm").iterdir()]
    for file_name in generated_project_files("dotfm"):
        assert file_name in project_files


def test_start_project_in_directory(runner: CommandRunner, tmp_path):
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
    # sourcery skip: no-loop-in-tests
    project_files = [file.name for file in project_dir.iterdir()]
    for file_name in generated_project_files("dotfm"):
        assert file_name in project_files


def test_start_project_in_directory_with_root(runner: CommandRunner, tmp_path):
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
    # sourcery skip: no-loop-in-tests
    project_files = [file.name for file in project_dir.iterdir()]
    for file_name in generated_project_files("dotfm"):
        assert file_name in project_files


def test_user_name_and_email(runner: CommandRunner, git_user_infos):
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


# def test_no_git_installed(runner: CommandRunner, tmp_path):
#     origina_run = subprocess.run
#
#     def mock_run(*args, **kwargs):
#         if args[0][0] != "git":
#             return origina_run(*args, **kwargs)
#         mock = Mock()
#         mock.returncode = 1
#         return mock
#
#     with patch("subprocess.run", side_effect=mock_run):
#         runner.invoke(
#             "start-project",
#             "dotfm",
#             "--skip-new-version-check",
#             "--blueprint",
#             str(blueprint_path),
#         )
#         assert Path("dotfm").exists()
#         config = read_falco_config(Path("dotfm/pyproject.toml"))
#         config_keys = config.keys()
#         assert "utils_path" in config.get("crud")
#         assert "work" in config_keys
#
#         # sourcery skip: no-loop-in-tests
#         project_files = [file.name for file in Path("dotfm").iterdir()]
#         for file_name in generated_project_files("dotfm"):
#             assert file_name in project_files


# def test_no_internet_access(runner: CommandRunner):
#     with mock.patch("socket.socket", side_effect=OSError("Network access is cut off")):
#         runner.invoke("start-project", "dotfm", "--skip-new-version-check")
#     assert Path("dotfm").exists()
#     # sourcery skip: no-loop-in-tests
#     project_files = [file.name for file in Path("dotfm").iterdir()]
#     for file_name in generated_project_files("dotfm"):
#         assert file_name in project_files
