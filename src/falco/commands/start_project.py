from __future__ import annotations

import json
import os
import shutil
import subprocess
from contextlib import contextmanager
from contextlib import suppress
from pathlib import Path
from typing import Annotated

import cappa
import httpx
from cookiecutter.exceptions import CookiecutterException
from cruft import create
from cruft.exceptions import InvalidCookiecutterRepository
from falco.commands import InstallCrudUtils
from falco.commands.crud.utils import run_html_formatters
from falco.commands.htmx import get_latest_tag as htmx_latest_tag
from falco.commands.htmx import Htmx
from falco.config import read_falco_config
from falco.config import write_falco_config
from falco.utils import clean_project_name
from falco.utils import is_new_falco_cli_available
from falco.utils import RICH_INFO_MARKER
from falco.utils import RICH_SUCCESS_MARKER
from falco.utils import simple_progress
from rich import print as rich_print
from rich.prompt import Prompt

DEFAULT_SKIP = [
    "playground.ipynb",
    "README.md",
]


def get_authors_info() -> tuple[str, str]:
    default_author_name = "Tobi DEGNON"
    default_author_email = "tobidegnon@proton.me"
    git_config_cmd = ["git", "config", "--global", "--get"]
    try:
        user_name_cmd = subprocess.run([*git_config_cmd, "user.name"], capture_output=True, text=True, check=False)
        user_email_cmd = subprocess.run([*git_config_cmd, "user.email"], capture_output=True, text=True, check=False)
    except FileNotFoundError:
        return default_author_name, default_author_email
    if user_email_cmd.returncode != 0:
        return default_author_name, default_author_email
    return (
        user_name_cmd.stdout.strip("\n"),
        user_email_cmd.stdout.strip("\n"),
    )


@contextmanager
def change_directory(new_directory):
    current_directory = Path.cwd()
    try:
        os.chdir(new_directory)
        yield
    finally:
        os.chdir(current_directory)


@cappa.command(help="Initialize a new django project the falco way.")
class StartProject:
    project_name: Annotated[
        str,
        cappa.Arg(parse=clean_project_name, help="Name of the project to create."),
    ]
    directory: Annotated[Path | None, cappa.Arg(help="Directory to create project in.")]
    is_root: Annotated[
        bool,
        cappa.Arg(
            default=False,
            short="-r",
            long="--root",
            help="Consider the specified directory as the root directory.",
        ),
    ]
    skip_new_version_check: Annotated[
        bool,
        cappa.Arg(
            default=False,
            long="--skip-new-version-check",
            help="Do not check for new version.",
        ),
    ]
    blueprint: Annotated[
        str,
        cappa.Arg(
            default="https://github.com/Tobi-De/falco_blueprint_basic.git",
            long="--blueprint",
            short="-b",
            help="The blueprint to use to generate the project.",
        ),
    ]

    def __call__(self) -> None:
        if self.is_root and not self.directory:
            raise cappa.Exit("You need to specify a directory when using the --root flag.", code=1)
        if not self.skip_new_version_check and is_new_falco_cli_available():
            message = (
                f"{RICH_INFO_MARKER} A new version of falco-cli is available. To upgrade, run "
                f"[green]pip install -U falco-cli."
            )
            rich_print(message)

            response = Prompt.ask(
                f"{RICH_INFO_MARKER}Do you want to stop to upgrade your current falco-cli version? (Y/n)",
                default="Y",
            )

            if response.lower() == "y":
                rich_print(
                    f"{RICH_INFO_MARKER}To see the latest features and improvements, "
                    f"visit https://github.com/Tobi-De/falco/releases."
                )
                raise cappa.Exit(code=0)

        project_dir = self.init_project()
        with change_directory(project_dir):
            pyproject_path = Path("pyproject.toml")
            falco_config = read_falco_config(pyproject_path)
            crud_utils = InstallCrudUtils().install(project_name=self.project_name, falco_config=falco_config)
            config = {
                "crud_utils": str(crud_utils),
                **self.cruft_file_to_falco_config(),
            }
            with suppress(cappa.Exit, httpx.TimeoutException, httpx.ConnectError):
                version = htmx_latest_tag()
                filepath = Htmx().download(version=htmx_latest_tag(), falco_config=falco_config)
                config["htmx"] = Htmx.format_for_config(filepath, version)

            write_falco_config(pyproject_path=pyproject_path, **config)

        run_html_formatters(project_dir / self.project_name / "templates")

        msg = f"{RICH_SUCCESS_MARKER} Project initialized, keep up the good work!\n"
        msg += (
            f"{RICH_INFO_MARKER} If you like the project consider dropping a star at "
            f"https://github.com/Tobi-De/falco"
        )

        rich_print(msg)

    def init_project(self) -> Path:
        author_name, author_email = get_authors_info()
        with simple_progress("Initializing your new django project... :sunglasses:"):
            try:
                project_dir = create(
                    self.blueprint,
                    no_input=True,
                    output_dir=self.directory or Path(),
                    extra_context={
                        "project_name": self.project_name,
                        "author_name": author_name,
                        "author_email": author_email,
                    },
                )
            except CookiecutterException as e:
                msg = str(e).replace("Error:", "")
                raise cappa.Exit(msg, code=1) from e
            except InvalidCookiecutterRepository as e:
                raise cappa.Exit("Network error, check your internet connection.", code=1) from e

            if self.is_root:
                renamed_project_dir = self.directory / "tmp_renamed_dir"
                shutil.move(project_dir, renamed_project_dir)
                for obj in Path(renamed_project_dir).iterdir():
                    shutil.move(obj, self.directory)
                renamed_project_dir.rmdir()
                project_dir = self.directory

        return project_dir

    def cruft_file_to_falco_config(self) -> dict:
        cruft_file = Path(".cruft.json")
        cruft_state = json.loads(cruft_file.read_text())
        cruft_file.unlink()
        return {
            "revision": cruft_state["commit"],
            "skip": DEFAULT_SKIP,
            "blueprint": self.blueprint,
        }
