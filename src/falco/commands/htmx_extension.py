from pathlib import Path
from typing import Annotated

import cappa
import httpx
from falco.config import read_falco_config
from falco.utils import get_pyproject_file
from falco.utils import network_request_with_progress
from falco.utils import simple_progress
from rich import print as rich_print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .htmx import Htmx

REGISTRY_URL = "https://htmx-extensions.oluwatobi.dev/extensions.json"


@cappa.command(help="Download one of htmx extensions.", name="htmx-ext")
class HtmxExtension:
    name: Annotated[
        str | None,
        cappa.Arg(
            default=None,
            help="The name of the extension to download.",
        ),
    ]
    output: Annotated[
        Path | None,
        cappa.Arg(
            default=None,
            help="The directory to write the downloaded file to.",
            short="-o",
            long="--output",
        ),
    ]

    def __call__(self) -> None:
        if self.name:
            self.download()
        else:
            self.list_all()

    def download(self):
        extensions = self.read_registry()
        extension = extensions.get(self.name)

        if not extension:
            msg = f"Could not find {self.name} extension."
            raise cappa.Exit(msg, code=1)

        with simple_progress(f"Downloading {self.name} extension"):
            download_url = extension.get("download_url")
            response = httpx.get(download_url, follow_redirects=True)

            output_file = self.resolve_filepath()
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(response.text)

        rich_print(
            Panel(
                f"[green]Extension {self.name} downloaded successfully![/green]",
                subtitle=extension.get("doc_url"),
            )
        )

    def resolve_filepath(self) -> Path:
        try:
            pyproject_path = get_pyproject_file()
        except cappa.Exit:
            pyproject_path = None

        if self.output:
            return self.output if self.output.name.endswith(".js") else self.output / f"{self.name}.js"

        if self.output is None and pyproject_path:
            falco_config = read_falco_config(pyproject_path=pyproject_path)
            htmx_config = Htmx.read_from_config(falco_config=falco_config)
            htmx_filepath, _ = htmx_config
            return htmx_filepath.parent / f"{self.name}.js"

        return Path(f"{self.name}.js")

    def list_all(self):
        extensions = self.read_registry()

        table = Table(
            title="Htmx Extensions",
            caption="Full details at https://htmx-extensions.oluwatobi.dev",
            show_lines=True,
        )

        table.add_column("Name", style="green")
        table.add_column("Description", style="magenta")

        for name, metadata in extensions.items():
            table.add_row(name, metadata.get("description", ""))

        console = Console()
        console.print(table)

    @classmethod
    def read_registry(cls):
        with network_request_with_progress(REGISTRY_URL, "Loading extensions registry") as response:
            import time

            time.sleep(2)
            return response.json()
