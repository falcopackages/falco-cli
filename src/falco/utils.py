import ast
import importlib.util
import subprocess
from contextlib import contextmanager
from pathlib import Path
from typing import TypedDict

import cappa
import httpx
from falco import falco_version
from rich.progress import Progress
from rich.progress import SpinnerColumn
from rich.progress import TextColumn
from tomlkit import parse

RICH_SUCCESS_MARKER = "[green]SUCCESS:"
RICH_ERROR_MARKER = "[red]ERROR:"
RICH_INFO_MARKER = "[blue]INFO:"
RICH_COMMAND_MARKER = "[yellow]"
RICH_COMMAND_MARKER_END = "[/yellow]"


class FalcoConfig(TypedDict):
    revision: str
    blueprint: str
    skip: list[str]
    work: dict[str, str]


def default_falco_config() -> FalcoConfig:
    return {
        "revision": "f018c4c5184b8f10ddc2110ef6b75d556c2b29cd",
        "blueprint": "https://github.com/Tobi-De/falco_blueprint_basic.git",
        "skip": [
            "playground.ipynb",
            "README.md",
        ],
        "work": {
            "server": "python manage.py migrate && python manage.py tailwind runserver"
        },
    }


def get_crud_blueprints_path() -> Path:
    package = importlib.util.find_spec("falco")
    if package is None:
        raise cappa.Exit("The falco base install path could not be found.", code=1)
    return Path(package.submodule_search_locations[0])


def clean_project_name(val: str) -> str:
    return val.strip().replace(" ", "_").replace("-", "_")


def get_project_name():
    try:
        pyproject = parse(Path("pyproject.toml").read_text())
    except FileNotFoundError as e:
        raise cappa.Exit("The pyproject.toml could not be found.", code=1) from e

    return pyproject["project"]["name"]


def get_author_info():
    try:
        pyproject = parse(Path("pyproject.toml").read_text())
    except FileNotFoundError as e:
        raise cappa.Exit("The pyproject.toml could not be found.", code=1) from e

    return pyproject["project"]["authors"][0]


@contextmanager
def simple_progress(
    description: str, display_text="[progress.description]{task.description}"
):
    progress = Progress(SpinnerColumn(), TextColumn(display_text), transient=True)
    progress.add_task(description=description, total=None)
    try:
        yield progress.start()
    finally:
        progress.stop()


@contextmanager
def network_request_with_progress(url: str, description: str):
    try:
        with simple_progress(description):
            yield httpx.get(url)
    except httpx.ConnectError as e:
        raise cappa.Exit(f"Connection error, {url} is not reachable.", code=1) from e


class ShellCodeError(Exception):
    pass


def run_in_shell(command: str, eval_result: bool = True):
    result = subprocess.run(
        ["python", "manage.py", "shell", "-c", command],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise ShellCodeError(result.stderr)
    return ast.literal_eval(result.stdout) if eval_result else result.stdout


def is_git_repo_clean() -> bool:
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"], capture_output=True, text=True, check=True
        )
        return result.stdout.strip() == ""
    except subprocess.CalledProcessError:
        return False


def is_new_falco_cli_available(fail_on_error: bool = False) -> bool:
    try:
        with network_request_with_progress(
            "https://pypi.org/pypi/falco-cli/json",
            "Checking for new falco version...",
        ) as response:
            latest_version = response.json()["info"]["version"]
            current_version = falco_version
            return latest_version != current_version
    except cappa.Exit:
        if fail_on_error:
            raise
        return False
