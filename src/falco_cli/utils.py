import subprocess
from contextlib import contextmanager

from rich.progress import Progress
from rich.progress import SpinnerColumn
from rich.progress import TextColumn

# Formatter stubs — overridden at runtime when optional formatters are available
def run_html_formatters(*_, **__):
    pass


def run_python_formatters(*_, **__):
    pass


@contextmanager
def simple_progress(description: str, display_text="[progress.description]{task.description}"):
    progress = Progress(SpinnerColumn(), TextColumn(display_text), transient=True)
    progress.add_task(description=description, total=None)
    try:
        yield progress.start()
    finally:
        progress.stop()


