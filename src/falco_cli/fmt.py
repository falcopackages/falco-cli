from pathlib import Path
from typing import Annotated

import cappa

from .utils import run_html_formatters, run_python_formatters, simple_progress


@cappa.command(help="Format code files using specified formatters.")
class Fmt:
    filepath: Annotated[Path, cappa.Arg(help="Path to the file to format.")] = None
    python: Annotated[
        bool,
        cappa.Arg(
            False,
            short="-p",
            long="--python",
            help="Run Python formatters only.",
        ),
    ] = False
    html: Annotated[
        bool,
        cappa.Arg(
            False,
            short="-t",
            long="--html",
            help="Run HTML formatters only.",
        ),
    ] = False

    def __call__(self):
        filepath = self.filepath or Path()

        if not self.html:
            with simple_progress("Running python formatters"):
                run_python_formatters(filepath)
        if not self.python:
            with simple_progress("Running html formatters"):
                run_html_formatters(filepath)
