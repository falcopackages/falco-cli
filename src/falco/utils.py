from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path

import cappa
import httpx
import tomli_w
from rich.progress import Progress, SpinnerColumn, TextColumn

RICH_SUCCESS_MARKER = "[green]SUCCESS:"
RICH_ERROR_MARKER = "[red]ERROR:"
RICH_INFO_MARKER = "[blue]INFO:"
RICH_COMMAND_MARKER = "[yellow]"
RICH_COMMAND_MARKER_END = "[/yellow]"

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


def clean_project_name(val: str) -> str:
    return val.strip().replace(" ", "_").replace("-", "_")


def get_current_dir_as_project_name():
    current_dir = Path().resolve(strict=True).stem
    return clean_project_name(current_dir)


def read_toml(file: Path) -> dict:
    return tomllib.loads(file.read_text())


def write_toml(file: Path, data: dict) -> None:
    remove_empty_top_level_table(data)
    sorted_data = sort_config(data)
    file.write_text(tomli_w.dumps(sorted_data))


def sort_config(config: dict) -> dict:
    return dict(sorted(config.items()))


def remove_empty_top_level_table(config: dict) -> None:
    config_copy = deepcopy(config)
    for key, value in config_copy.items():
        if not value:
            config.pop(key)


def download_archive(url: str, dest: Path) -> None:
    with httpx.stream("GET", url, follow_redirects=True) as response:
        with open(dest, "wb") as archive_file:
            for chunk in response.iter_bytes():
                archive_file.write(chunk)


@contextmanager
def simple_progress(description: str, display_text="[progress.description]{task.description}"):
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
