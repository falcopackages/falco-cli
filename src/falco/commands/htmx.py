from __future__ import annotations

from pathlib import Path
from typing import Annotated

import cappa
from falco.config import read_falco_config
from falco.config import write_falco_config
from falco.utils import get_pyproject_file
from falco.utils import network_request_with_progress
from httpx import codes
from rich import print as rich_print
from rich.panel import Panel

HTMX_DOWNLOAD_URL = "https://unpkg.com/htmx.org@{version}/dist/htmx.min.js"
HTMX_GH_RELEASE_LATEST_URL = "https://api.github.com/repos/bigskysoftware/htmx/releases/latest"

HtmxConfig = tuple[Path, str | None]


def get_latest_tag() -> str:
    with network_request_with_progress(HTMX_GH_RELEASE_LATEST_URL, "Getting htmx latest version") as response:
        try:
            return response.json()["tag_name"][1:]
        except KeyError as e:
            msg = (
                "Unable to retrieve the latest version of htmx. "
                "This issue may be due to reaching the GitHub API rate limit. Please try again later."
            )
            raise cappa.Exit(msg, code=1) from e


@cappa.command(help="Download the latest version (if no version is specified) of htmx.")
class Htmx:
    version: Annotated[str, cappa.Arg(default="latest")] = "latest"
    output: Annotated[Path | None, cappa.Arg(default=None, short="-o", long="--output")] = None

    def __call__(self):
        latest_version = get_latest_tag()
        version = self.version if self.version != "latest" else latest_version

        try:
            pyproject_path = get_pyproject_file()
            falco_config = read_falco_config(pyproject_path)
        except cappa.Exit:
            falco_config = {}
            pyproject_path = None

        filepath = self.download(version, falco_config=falco_config)
        if pyproject_path:
            write_falco_config(
                pyproject_path=pyproject_path,
                htmx=self.format_for_config(filepath, version),
            )

        subtitle = (
            "You are using the latest version of htmx."
            if version == latest_version
            else f"The latest version available is {latest_version}"
        )

        rich_print(
            Panel(
                f"[green]htmx version {version} downloaded successfully to {filepath} ![/green]",
                subtitle=subtitle,
            )
        )

    @classmethod
    def format_for_config(cls, filepath: Path, version: str | None) -> str:
        return str(filepath) if version is None else f"{filepath}:{version}"

    def download(self, version: str, falco_config: dict) -> Path:
        url = HTMX_DOWNLOAD_URL.format(version=version)

        with network_request_with_progress(url, f"Downloading htmx version {version}") as response:
            content = response.content.decode("utf-8")
            if response.status_code == codes.NOT_FOUND:
                msg = f"Could not find htmx version {version}."
                raise cappa.Exit(msg, code=1)

        filepath = self.resolve_filepath(falco_config=falco_config)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content)
        return filepath

    def resolve_filepath(self, falco_config: dict) -> Path:
        if self.output:
            filepath = self.output if str(self.output).endswith(".js") else self.output / "htmx.min.js"
        elif self.output is None and "htmx" in falco_config:
            htmx_config = self.read_from_config(falco_config)
            filepath, _ = htmx_config
        else:
            filepath = Path("htmx.min.js")

        return filepath

    @classmethod
    def read_from_config(cls, falco_config: dict) -> HtmxConfig:
        htmx = falco_config.get("htmx")
        if not htmx:
            return Path("htmx.min.js"), None

        try:
            filepath, version = htmx.split(":")
        except ValueError:
            return Path(htmx), None

        return Path(filepath), version
