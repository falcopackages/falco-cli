from pathlib import Path
from typing import Annotated
from typing import Set

import cappa
import tomlkit
from falco.utils import default_falco_config
from falco.utils import FalcoConfig
from falco.utils import get_project_name
from falco.utils import is_git_repo_clean
from falco.utils import is_new_falco_cli_available
from falco.utils import RICH_INFO_MARKER
from falco.utils import RICH_SUCCESS_MARKER
from rich import print as rich_print


# TODO add  --diff to just check diff without update


def cruft_state_from(
    config: FalcoConfig, project_name: str, author_name: str, author_email: str
) -> dict:
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
                "_template": config["blueprint"],
            }
        },
        "directory": None,
    }


@cappa.command(help="Update your project with changes from falco.")
class Update:
    init: Annotated[
        bool,
        cappa.Arg(
            default=False, short="-i", long="--init", help="Initialize falco config."
        ),
    ]

    def __call__(
        self, project_name: Annotated[str, cappa.Dep(get_project_name)]
    ) -> None:
        if is_new_falco_cli_available(fail_on_error=True):
            raise cappa.Exit(
                "You need have the latest version of falco-cli to update.", code=1
            )

        if not is_git_repo_clean():
            raise cappa.Exit(
                "Update cannot be applied on an unclean git repo. Please commit or stash"
                " your changes before running this command.",
                code=1,
            )

        pyproject_path = Path("pyproject.toml")
        try:
            pyproject = tomlkit.parse(pyproject_path.read_text())
        except FileNotFoundError as e:
            raise cappa.Exit(
                "Could not find a pyproject.toml file in the current directory.", code=1
            ) from e

        if self.init:
            existing_config = pyproject["tool"].get("falco", {})
            existing_config.update(default_falco_config())
            pyproject["tool"]["falco"] = existing_config
            pyproject_path.write_text(tomlkit.dumps(pyproject))
            rich_print(f"{RICH_SUCCESS_MARKER} Initialized falco config.")
            raise cappa.Exit()

        last_commit = self._update(
            cruft_state=cruft_state_from(
                config=pyproject["tool"]["falco"],
                project_name=project_name,
                author_name=pyproject["project"]["authors"][0]["name"],
                author_email=pyproject["project"]["authors"][0]["email"],
            )
        )
        if last_commit is None:
            rich_print(
                f"{RICH_INFO_MARKER} Nothing to do, project is already up to date!"
            )
            raise cappa.Exit(code=0)
        pyproject["tool"]["falco"]["revision"] = last_commit
        pyproject_path.write_text(tomlkit.dumps(pyproject))
        rich_print(
            f"{RICH_SUCCESS_MARKER} Great! Your project has been updated to the latest version!"
        )

    def _update(self, cruft_state: dict, project_dir: Path = Path(".")) -> str | None:
        """The update function from cruft"""
        from cruft._commands.utils.iohelper import AltTemporaryDirectory
        from cruft._commands import utils
        from cruft._commands.update import _apply_project_updates

        directory = "repo"
        skip_apply_ask = True
        skip_update = False
        allow_untracked_files = False
        strict = True

        with AltTemporaryDirectory(directory) as tmpdir_:
            # Initial setup
            tmpdir = Path(tmpdir_)
            repo_dir = tmpdir / "repo"
            current_template_dir = tmpdir / "current_template"
            new_template_dir = tmpdir / "new_template"
            deleted_paths: Set[Path] = set()
            # Clone the template
            with utils.cookiecutter.get_cookiecutter_repo(
                cruft_state["template"], repo_dir
            ) as repo:
                last_commit = repo.head.object.hexsha

                # Bail early if the repo is already up to date and no inputs are asked
                if utils.cruft.is_project_updated(
                    repo, cruft_state["commit"], last_commit, strict=strict
                ):
                    return None

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
                return last_commit
