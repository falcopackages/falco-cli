import json
import secrets
from contextlib import contextmanager
from pathlib import Path
from typing import Annotated
from typing import Any

import cappa
import tomlkit
import typer
from cruft import diff as cruft_diff
from cruft._commands import utils
from cruft._commands.update import _apply_project_updates
from cruft._commands.utils.iohelper import AltTemporaryDirectory
from . import checks
from .config import FalcoConfig
from .utils import get_project_name
from .utils import get_username
from .utils import RICH_INFO_MARKER
from .utils import RICH_SUCCESS_MARKER
from rich import print as rich_print


@contextmanager
def cruft_file(cruft_state: dict):
    file_path = Path(".cruft.json")
    try:
        file_path.write_text(json.dumps(cruft_state))
        yield
    finally:
        file_path.unlink()


def cruft_state_from(config: FalcoConfig, project_name: str, author_name: str, author_email: str) -> dict:
    return {
        "template": config["blueprint"],
        "commit": config["revision"],
        "skip": config["skip"],
        "checkout": None,
        "context": {
            "cookiecutter": {
                "project_name": project_name,
                "author_name": author_name,
                "author_email": author_email,
                "username": get_username(),
                "secret_key": secrets.token_hex(24),
                "_template": config["blueprint"],
            }
        },
        "directory": None,
    }


@cappa.command(help="Update your project with changes from falco.")
class UpdateProject:
    diff: Annotated[
        bool,
        cappa.Arg(default=False, short="-d", long="--diff", help="Show diff of changes."),
    ]
    interactive: Annotated[
        bool,
        cappa.Arg(default=False, short="-i", long="--interactive", help="Interactive mode"),
    ]

    def __call__(self, project_name: Annotated[str, cappa.Dep(get_project_name)]) -> None:
        checks.clean_git_repo()

        pyproject_path = Path("pyproject.toml")
        try:
            pyproject = tomlkit.parse(pyproject_path.read_text())
        except FileNotFoundError as e:
            raise cappa.Exit("Could not find a pyproject.toml file in the current directory.", code=1) from e

        cruft_state = cruft_state_from(
            config=pyproject["tool"]["falco"],
            project_name=project_name,
            author_name=pyproject["project"]["authors"][0]["name"],
            author_email=pyproject["project"]["authors"][0]["email"],
        )

        if self.diff:
            with cruft_file(cruft_state):
                cruft_diff()
            raise cappa.Exit(code=0)

        with cruft_file(cruft_state):
            last_commit = cruft_update(allow_untracked_files=True, skip_apply_ask=not self.interactive)
        if last_commit is None:
            rich_print(f"{RICH_INFO_MARKER} Nothing to do, project is already up to date!")
            raise cappa.Exit(code=0)
        pyproject["tool"]["falco"]["revision"] = last_commit
        pyproject_path.write_text(tomlkit.dumps(pyproject))
        rich_print(f"{RICH_SUCCESS_MARKER} Great! Your project has been updated to the latest version!")


def cruft_update(
    project_dir: Path = Path("commands"),
    cookiecutter_input: bool = False,
    refresh_private_variables: bool = False,
    skip_apply_ask: bool = True,
    skip_update: bool = False,
    checkout: str | None = None,
    strict: bool = True,
    allow_untracked_files: bool = False,
    extra_context: dict[str, Any] | None = None,
    extra_context_file: Path | None = None,
) -> str:
    """Update specified project's cruft to the latest and greatest release."""
    cruft_file = utils.cruft.get_cruft_file(project_dir)

    if extra_context_file:
        if extra_context_file.samefile(cruft_file):
            typer.secho(
                f"The file path given to --variables-to-update-file cannot be the same as the"
                f" project's cruft file ({cruft_file}), as the update process needs"
                f" to know the old/original values of variables as well. Please specify a"
                f" different path, and the project's cruft file will be updated as"
                f" part of the process.",
                fg=typer.colors.RED,
            )
            return False

        extra_context_from_cli = extra_context
        with open(extra_context_file) as extra_context_fp:
            extra_context = json.load(extra_context_fp) or {}
        extra_context = extra_context.get("context") or {}
        extra_context = extra_context.get("cookiecutter") or {}
        if extra_context_from_cli:
            extra_context.update(extra_context_from_cli)

    cruft_state = json.loads(cruft_file.read_text())

    directory = cruft_state.get("directory", "")
    if directory:
        directory = str(Path("repo") / directory)
    else:
        directory = "repo"

    with AltTemporaryDirectory(directory) as tmpdir_:
        # Initial setup
        tmpdir = Path(tmpdir_)
        repo_dir = tmpdir / "repo"
        current_template_dir = tmpdir / "current_template"
        new_template_dir = tmpdir / "new_template"
        deleted_paths: set[Path] = set()
        # Clone the template
        with utils.cookiecutter.get_cookiecutter_repo(cruft_state["template"], repo_dir, checkout) as repo:
            last_commit = repo.head.object.hexsha

            # Bail early if the repo is already up to date and no inputs are asked
            if not (
                extra_context or cookiecutter_input or refresh_private_variables
            ) and utils.cruft.is_project_updated(repo, cruft_state["commit"], last_commit, strict):
                typer.secho(
                    "Nothing to do, project's cruft is already up to date!",
                    fg=typer.colors.GREEN,
                )
                return True

            # Generate clean outputs via the cookiecutter
            # from the current cruft state commit of the cookiecutter and the updated
            # cookiecutter.
            # For the current cruft state, we do not try to update the cookiecutter_input
            # because we want to keep the current context input intact.
            _ = utils.generate.cookiecutter_template(
                output_dir=current_template_dir,
                repo=repo,
                cruft_state=cruft_state,
                project_dir=project_dir,
                checkout=cruft_state["commit"],
                deleted_paths=deleted_paths,
                update_deleted_paths=True,
            )
            # Remove private variables from cruft_state to refresh their values
            # from the cookiecutter template config
            # if refresh_private_variables:
            #     _clean_cookiecutter_private_variables(cruft_state)

            # Add new input data from command line to cookiecutter context
            if extra_context:
                extra = cruft_state["context"]["cookiecutter"]
                for k, v in extra_context.items():
                    extra[k] = v

            new_context = utils.generate.cookiecutter_template(
                output_dir=new_template_dir,
                repo=repo,
                cruft_state=cruft_state,
                project_dir=project_dir,
                cookiecutter_input=cookiecutter_input,
                checkout=last_commit,
                deleted_paths=deleted_paths,
            )

        # Given the two versions of the cookiecutter outputs based
        # on the current project's context we calculate the diff and
        # apply the updates to the current project.
        if _apply_project_updates(
            current_template_dir,
            new_template_dir,
            project_dir,
            skip_update,
            skip_apply_ask,
            allow_untracked_files,
        ):
            # Update the cruft state and dump the new state
            # to the cruft file
            cruft_state["commit"] = last_commit
            cruft_state["checkout"] = checkout
            cruft_state["context"] = new_context
            cruft_file.write_text(utils.cruft.json_dumps(cruft_state))
            # typer.secho(
            #     "Good work! Project's cruft has been updated and is as clean as possible!",
            #     fg=typer.colors.GREEN,
            # )
        return last_commit
