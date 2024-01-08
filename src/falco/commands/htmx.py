from __future__ import annotations

from pathlib import Path
from typing import Annotated

import cappa
from falco.utils import network_request_with_progress
from rich import print as rich_print
from rich.panel import Panel

HTMX_DOWNLOAD_URL = "https://unpkg.com/htmx.org@{version}/dist/htmx.min.js"
HTMX_GH_RELEASE_LATEST_URL = "https://api.github.com/repos/bigskysoftware/htmx/releases/latest"


def get_latest_tag(fail_silently) -> str:
    with network_request_with_progress(HTMX_GH_RELEASE_LATEST_URL, "Getting latest version", fail_silently) as response:
        if response:
            return response.json()["tag_name"][1:]
        return "latest"


@cappa.command(help="Download the latest version (if no version is specified) of htmx.")
class Htmx:
    version: Annotated[str, cappa.Arg(default="latest")]
    output: Annotated[Path, cappa.Arg(default=Path("htmx.min.js"), short="-o", long="--output")]
    fail_silently: Annotated[bool, cappa.Arg(default=False, short="-f", long="--fail-silently")]

    def __call__(self):
        latest_version = get_latest_tag(self.fail_silently)
        version = self.version if self.version != "latest" else latest_version
        url = HTMX_DOWNLOAD_URL.format(version=version)
        with network_request_with_progress(url, f"Downloading htmx version {version}", self.fail_silently) as response:
            content = None
            if response:
                content = response.content.decode("utf-8")
                if response.status_code == 404:
                    raise cappa.Exit(f"Could not find htmx version {version}.", code=1)
        filepath = self.output if str(self.output).endswith(".js") else self.output / "htmx.min.js"
        if content:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            filepath.write_text(content)

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
        else:
            subtitle = (
                "You are using the default version of htmx."
            )
            rich_print(
                Panel(
                    f"[green]htmx with default version added successfully to {filepath} ![/green]\n[red]If you want to update the version, run the command [/red]\n[blue]falco htmx --output <path/to/htmx/>[/blue]",
                    subtitle=subtitle,
                )
            )
