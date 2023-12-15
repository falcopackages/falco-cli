from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Annotated

import cappa
from dict_deep import deep_set
from rich import print as rich_print
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt


from falco.utils import RICH_INFO_MARKER, RICH_SUCCESS_MARKER, clean_project_name, read_toml, simple_progress, write_toml

try:
    from enum import StrEnum
except ImportError:
    from enum import Enum

    class StrEnum(str, Enum):
        pass


@cappa.command(help="Initialize a new django project.")
class StartProject:
    project_name: Annotated[
        str,
        cappa.Arg(parse=clean_project_name),
    ]

    def __post_init__(self):
        self.project_path = Path(self.project_name)

    def __call__(self) -> None:
        if self.project_path.exists():
            raise cappa.Exit(
                f"A directory with the name {self.project_name} already exists in the current directory", code=1
            )

        self.init_project()

        self.update_authors()

        if self.branch != "main":
            self.apply_branch_patch()

        if Prompt.ask("Do you want to install the dependencies? (y/N)", choices=["y", "n"]) == "y":
            self.install_dependencies()

        msg = f"{RICH_SUCCESS_MARKER} Project initialized, keep up the good work!\n"
        msg += (
            f"{RICH_INFO_MARKER} If you like the project consider dropping a star at "
            f"https://github.com/Tobi-De/falco"
        )

        rich_print(msg)

    def init_project(self) -> None:
        with simple_progress("Initializing your new django project... :sunglasses:"):
            if template_dir := get_template_dir(self.branch):
                # run the django-admin command
                subprocess.run(
                    [
                        "django-admin",
                        "startproject",
                        self.project_name,
                        "--template",
                        template_dir,
                        "-e=py,html,toml,md,json,js,sh",
                        "--exclude=docs",
                        "--exclude=fuzzy_couscous",
                        "--exclude=.github",
                        "--exclude=.idea",
                    ]
                )

            else:
                raise cappa.Exit("Couldn't download or find the template to use, check your connection.")

    def update_authors(self) -> None:
        name, email = self.get_git_user_infos()
        if not name:
            name = Prompt.ask("Enter your name")
        if not email:
            email = Prompt.ask("Enter your email")
        pyproject_file = self.project_path / "pyproject.toml"
        project_config = read_toml(self.project_path / "pyproject.toml")
        deep_set(project_config, "tool.poetry.authors", [f"{name} <{email}>"])
        write_toml(pyproject_file, project_config)

    def apply_branch_patch(self) -> None:
        pass

    def install_dependencies(self) -> None:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Installing dependencies... :boom:", total=None)
            subprocess.call(
                ["poetry install --with dev"],
                cwd=self.project_path,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=True,
            )

    @staticmethod
    def get_git_user_infos():
        git_config_cmd = ["git", "config", "--global", "--get"]
        try:
            user_name_cmd = subprocess.run(git_config_cmd + ["user.name"], capture_output=True, text=True)
            user_email_cmd = subprocess.run(git_config_cmd + ["user.email"], capture_output=True, text=True)
        except FileNotFoundError:
            return None
        if user_email_cmd.returncode != 0:
            return None
        return (
            user_name_cmd.stdout.strip("\n"),
            user_email_cmd.stdout.strip("\n"),
        )
