from __future__ import annotations

import os
import secrets
import shutil
import subprocess
from contextlib import contextmanager
from pathlib import Path
from typing import Annotated

import cappa
from cookiecutter.config import get_user_config
from cookiecutter.exceptions import CookiecutterException
from cookiecutter.main import cookiecutter

from .config import write_falco_config
from .utils import clean_project_name
from .utils import is_new_falco_cli_available
from .utils import get_username
from .utils import RICH_INFO_MARKER
from .utils import RICH_SUCCESS_MARKER
from .utils import simple_progress
from rich import print as rich_print
from rich.prompt import Prompt

DEFAULT_SKIP = ["playground.ipynb", "README.md", "*/static/*"]


@simple_progress("Running html formatters")
def run_html_formatters(filepath: str | Path):
    djlint = ["djlint", filepath, "--reformat"]
    subprocess.run(djlint, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)


@cappa.command(help="Initialize a new django project the falco way.")
class StartProject:
    project_name: Annotated[
        str,
        cappa.Arg(parse=clean_project_name, help="Name of the project to create."),
    ]
    directory: Annotated[Path | None, cappa.Arg(help="Directory to create project in.")] = None
    is_root: Annotated[
        bool,
        cappa.Arg(
            default=False,
            short="-r",
            long="--root",
            help="Consider the specified directory as the root directory.",
        ),
    ] = False
    skip_new_version_check: Annotated[
        bool,
        cappa.Arg(
            default=False,
            long="--skip-new-version-check",
            help="Do not check for new version.",
        ),
    ] = False
    blueprint: Annotated[
        str,
        cappa.Arg(
            default="tailwind",
            long="--blueprint",
            short="-b",
            help="The blueprint to use to generate the project.",
        ),
    ] = "tailwind"
    local: Annotated[
        bool,
        cappa.Arg(
            default=False,
            long="--local",
            short="-l",
            help="Use a local copy of the blueprint if it exists.",
        ),
    ] = False
    checkout: Annotated[str | None, cappa.Arg(default=None, long="--checkout", short="-c", hidden=True)] = None

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
                    f"visit https://github.com/falcopackages/falco-cli/releases."
                )
                raise cappa.Exit(code=0)

        with simple_progress("Resolving blueprint..."):
            self.blueprint, revision = resolve_blueprint(self.blueprint, use_local=self.local)
        project_dir = self.init_project()
        with change_directory(project_dir):
            pyproject_path = Path("pyproject.toml")
            env_file = Path(".env")
            env_file.touch()
            env_file.write_text("DEBUG=True")

            config = {
                "revision": revision,
                "skip": DEFAULT_SKIP,
                "blueprint": self.blueprint,
            }

            write_falco_config(pyproject_path=pyproject_path, **config)

        run_html_formatters(project_dir / self.project_name / "templates")

        msg = f"{RICH_SUCCESS_MARKER} Project initialized, keep up the good work!\n"
        msg += (
            f"{RICH_INFO_MARKER} If you like the project consider dropping a star at "
            f"https://github.com/falcopackages/falco-cli"
        )

        rich_print(msg)

    def init_project(self) -> Path:
        author_name, author_email = get_authors_info()
        with simple_progress("Initializing your new django project... :sunglasses:"):
            try:
                project_dir = cookiecutter(
                    self.blueprint,
                    no_input=True,
                    output_dir=self.directory or Path(),
                    checkout=self.checkout,
                    extra_context={
                        "project_name": self.project_name,
                        "author_name": author_name,
                        "author_email": author_email,
                        "username": get_username(),
                        "secret_key": f"django-insecure-{secrets.token_urlsafe(32)}",
                    },
                )
            except CookiecutterException as e:
                msg = str(e).replace("Error:", "")
                raise cappa.Exit(msg, code=1) from e

            if self.is_root:
                renamed_project_dir = self.directory / "tmp_renamed_dir"
                shutil.move(project_dir, renamed_project_dir)
                for obj in Path(renamed_project_dir).iterdir():
                    shutil.move(obj, self.directory)
                renamed_project_dir.rmdir()
                project_dir = self.directory

        return Path(project_dir)


def find_local_cookiecutter(repo: str) -> Path | None:
    repo_name = repo.split("/")[-1].replace(".git", "")
    cookiecutters_dir = Path(get_user_config()["cookiecutters_dir"])
    if not cookiecutters_dir.exists():
        return None
    for directory in cookiecutters_dir.iterdir():
        if not directory.is_dir():
            continue
        is_empty = not list(directory.iterdir())
        if directory.is_dir() and not is_empty and directory.name == repo_name:
            return directory
    return None


def resolve_blueprint(blueprint: str, *, use_local: bool = False) -> tuple[str, str]:
    name_to_urls = {
        "tailwind": "https://github.com/falcopackages/starter-template",
        "bootstrap": "https://github.com/falcopackages/starter-template-bootstrap",
    }
    repo = name_to_urls.get(blueprint, blueprint)

    if repo.startswith("http") and use_local:
        if local_repo := find_local_cookiecutter(repo):
            repo = str(local_repo.resolve())
        else:
            msg = f"No internet connection and no local blueprint found for {repo}."
            raise cappa.Exit(msg, code=1)

    result = subprocess.run(
        ["git", "ls-remote", repo, "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        msg = f"Blueprint {blueprint} could not be downloaded."
        raise cappa.Exit(msg, code=1)
    revision = result.stdout.split("\n")[0].split()[0].strip()
    return repo, revision


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
def change_directory(new_directory: str | Path):
    current_directory = Path.cwd()
    try:
        os.chdir(new_directory)
        yield
    finally:
        os.chdir(current_directory)
