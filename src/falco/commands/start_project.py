from __future__ import annotations

import json
import shutil
import subprocess
from contextlib import suppress
from pathlib import Path
from typing import Annotated

import cappa
import httpx
from cookiecutter.exceptions import CookiecutterException
from cruft import create
from cruft.exceptions import InvalidCookiecutterRepository
from falco.commands.htmx import Htmx
from falco.utils import clean_project_name
from falco.utils import default_falco_config
from falco.utils import is_new_falco_cli_available
from falco.utils import RICH_INFO_MARKER
from falco.utils import RICH_SUCCESS_MARKER
from falco.utils import simple_progress
from rich import print as rich_print
from rich.prompt import Prompt
from tomlkit import parse


def get_authors_info() -> tuple[str, str]:
    default_author_name = "Tobi DEGNON"
    default_author_email = "tobidegnon@proton.me"
    git_config_cmd = ["git", "config", "--global", "--get"]
    try:
        user_name_cmd = subprocess.run(
            [*git_config_cmd, "user.name"], capture_output=True, text=True, check=False
        )
        user_email_cmd = subprocess.run(
            [*git_config_cmd, "user.email"], capture_output=True, text=True, check=False
        )
    except FileNotFoundError:
        return default_author_name, default_author_email
    if user_email_cmd.returncode != 0:
        return default_author_name, default_author_email
    return (
        user_name_cmd.stdout.strip("\n"),
        user_email_cmd.stdout.strip("\n"),
    )


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

    def __call__(self) -> None:
        if self.is_root and not self.directory:
            raise cappa.Exit(
                "You need to specify a directory when using the --root flag.", code=1
            )
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
        msg = f"{RICH_SUCCESS_MARKER} Project initialized, keep up the good work!\n"
        msg += (
            f"{RICH_INFO_MARKER} If you like the project consider dropping a star at "
            f"https://github.com/Tobi-De/falco"
        )

        rich_print(msg)
        self.update_htmx(project_dir)
        self.cruft_to_falco_state(project_dir)

    def init_project(self) -> Path:
        author_name, author_email = get_authors_info()
        with simple_progress("Initializing your new django project... :sunglasses:"):
            try:
                project_dir = create(
                    "https://github.com/Tobi-De/falco_blueprint_basic.git",
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
                raise cappa.Exit(
                    "Network error, check your internet connection.", code=1
                ) from e

            if self.is_root:
                project_dir = self.directory / self.project_name
                tmp_project_dir = self.directory / "tmp"
                shutil.move(project_dir, tmp_project_dir)
                for obj in tmp_project_dir.iterdir():
                    shutil.move(obj, self.directory)
                tmp_project_dir.rmdir()

        return project_dir

    def update_htmx(self, project_dir: Path):
        with suppress(cappa.Exit, httpx.TimeoutException, httpx.ConnectError):
            static_path = "static/vendors/htmx/htmx.min.js"
            base_path = project_dir if self.is_root else project_dir / self.project_name
            Htmx(version="latest", output=base_path / static_path)()

    def cruft_to_falco_state(self, project_dir: Path):
        cruft_file = (
            project_dir.parent / ".cruft.json"
            if self.is_root
            else project_dir / ".cruft.json"
        )
        pyproject = (
            project_dir.parent / "pyproject.toml"
            if self.is_root
            else project_dir / "pyproject.toml"
        )
        cruft_state = json.loads(cruft_file.read_text())
        pyproject_dict = parse(pyproject.read_text())
        config = default_falco_config()
        config.update({"revision": cruft_state["commit"]})
        pyproject_dict["tool"]["falco"] = config
        # pyproject.write_text(dumps(pyproject_dict)) TODO: comment out when update feature ready
        cruft_file.unlink()
