from __future__ import annotations

from pathlib import Path
from typing import Annotated

import cappa
from falco.utils import get_pyproject_file
from falco.utils import network_request_with_progress
from falco.utils import read_falco_config
from falco.utils import write_falco_config
from httpx import codes
from rich import print as rich_print
from rich.panel import Panel

HTMX_DOWNLOAD_URL = "https://unpkg.com/htmx.org@{version}/dist/htmx.min.js"
HTMX_GH_RELEASE_LATEST_URL = "https://api.github.com/repos/bigskysoftware/htmx/releases/latest"


HtmxConfig = tuple[Path, str | None]


def get_latest_tag() -> str:
    with network_request_with_progress(HTMX_GH_RELEASE_LATEST_URL, "Getting latest version") as response:
        return response.json()["tag_name"][1:]


@cappa.command(help="Download the latest version (if no version is specified) of htmx.")
class Htmx:
    version: Annotated[str, cappa.Arg(default="latest")] = "latest"
    output: Annotated[Path | None, cappa.Arg(default=None, short="-o", long="--output")] = None

    def __call__(self):
        latest_version = get_latest_tag()
        version = self.version if self.version != "latest" else latest_version
        url = HTMX_DOWNLOAD_URL.format(version=version)

        with network_request_with_progress(url, f"Downloading htmx version {version}") as response:
            content = response.content.decode("utf-8")
            if response.status_code == codes.NOT_FOUND:
                msg = f"Could not find htmx version {version}."
                raise cappa.Exit(msg, code=1)

        try:
            pyproject_path = get_pyproject_file()
        except cappa.Exit:
            pyproject_path = None

        filepath = self.resolve_filepath(pyproject_path=pyproject_path)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content)

        subtitle = (
            "You are using the latest version of htmx."
            if version == latest_version
            else f"The latest version available is {latest_version}"
        )

        if pyproject_path:
            write_falco_config(pyproject_path=pyproject_path, htmx=f"{filepath}:{version}")

        rich_print(
            Panel(
                f"[green]htmx version {version} downloaded successfully to {filepath} ![/green]",
                subtitle=subtitle,
            )
        )

    def resolve_filepath(self, pyproject_path: Path | None) -> Path:
        if self.output:
            filepath = self.output if str(self.output).endswith(".js") else self.output / "htmx.min.js"
        elif self.output is None and pyproject_path:
            htmx_config = self.read_from_config(get_pyproject_file())
            filepath, _ = htmx_config
        else:
            filepath = Path("htmx.min.js")

        return filepath

    @classmethod
    def read_from_config(cls, pyproject_path: Path) -> HtmxConfig:
        htmx = read_falco_config(pyproject_path).get("htmx", None)
        if not htmx:
            return Path("htmx.min.js"), None

        try:
            filepath, version = htmx.split(":")
        except ValueError:
            return Path(htmx), None

        return Path(filepath), version
