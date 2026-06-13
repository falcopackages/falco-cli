import os
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import TypeVar

from rich.progress import Progress
from rich.progress import SpinnerColumn
from rich.progress import TextColumn

ReturnType = TypeVar("ReturnType")

RICH_SUCCESS_MARKER = "[green]SUCCESS:"
RICH_ERROR_MARKER = "[red]ERROR:"
RICH_INFO_MARKER = "[blue]INFO:"


def clean_project_name(val: str) -> str:
    return val.strip().replace(" ", "_").replace("-", "_")


def get_username() -> str:
    try:
        return os.getlogin()
    except OSError:
        return os.getenv("USERNAME", "tobi")


def get_project_name() -> str:
    import tomlkit

    pyproject = tomlkit.parse(Path("pyproject.toml").read_text())
    return pyproject["project"]["name"]


def run_python_formatters(filepath: str | Path):
    pass


def run_html_formatters(filepath: str | Path):
    pass


exec_path = Path(sys.executable).parent


@contextmanager
def simple_progress(description: str, display_text="[progress.description]{task.description}"):
    progress = Progress(SpinnerColumn(), TextColumn(display_text), transient=True)
    progress.add_task(description=description, total=None)
    try:
        yield progress.start()
    finally:
        progress.stop()
