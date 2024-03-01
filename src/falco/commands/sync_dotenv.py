import os
import secrets
from pathlib import Path
from typing import Annotated

import cappa
import tomlkit
from falco.utils import get_project_name
from rich import print as rich_print
from rich.prompt import Prompt


@cappa.command(help="Synchronize the .env file with the .env.template file.")
class SyncDotenv:
    fill_missing: Annotated[
        bool,
        cappa.Arg(
            False,
            short="-f",
            long="--fill-missing",
            help="Prompt to fill missing values.",
        ),
    ] = False
    print_env: Annotated[
        bool,
        cappa.Arg(
            False,
            short="-p",
            long="--print-env",
            help="Print the updated .env file to the console without modifying it.",
        ),
    ] = False

    def __call__(self, project_name: Annotated[str, cappa.Dep(get_project_name)]):
        dotenv_file = Path(".env")
        dotenv_template_file = Path(".env.template")

        dotenv_content = dotenv_file.read_text() if dotenv_file.exists() else ""
        dotenv_template_content = dotenv_template_file.read_text() if dotenv_template_file.exists() else ""

        debug = os.getenv("DEBUG", "true").lower() == "true"

        base_config = {"DEBUG": True} if debug else self.get_prod_config(project_name)

        config = {
            **parse(dotenv_template_content),
            **base_config,
            **parse(dotenv_content),
        }

        if self.fill_missing:
            for key, value in config.items():
                if not value:
                    config[key.upper()] = Prompt.ask(f"{key}")

        dotenv_content = get_updated(dotenv_content, config)
        if self.print_env:
            rich_print(dotenv_content)
            return

        dotenv_file.touch(exist_ok=True)
        dotenv_file.write_text(dotenv_content)

        dotenv_template_content = get_updated(
            dotenv_template_content,
            {key: "" for key in config},
            keep_original=True,
            keep_whitespace=True,
        )
        dotenv_template_file.touch(exist_ok=True)
        dotenv_template_file.write_text(dotenv_template_content)

        rich_print(f"[green] {dotenv_file} and {dotenv_template_file} synchronised [/green]")

    def get_prod_config(self, project_name: str) -> dict:
        return {
            "DEBUG": False,
            "SECRET_KEY": secrets.token_urlsafe(64),
            "ALLOWED_HOSTS": f"{project_name}.com",
            "DJANGO_SUPERUSER_EMAIL": get_superuser_email(project_name),
            "DJANGO_SUPERUSER_PASSWORD": secrets.token_urlsafe(8),
        }


def get_superuser_email(project_name: str):
    pyproject_file = Path("pyproject.toml")
    if pyproject_file.exists():
        pyproject = tomlkit.parse(pyproject_file.read_text())
        if authors := pyproject.get("project", {}).get("authors", []):
            return authors[0]["email"]
    return f"admin@{project_name}.com"


def parse(env_content: str) -> dict:
    result = {}
    for line in env_content.split("\n"):
        stripped_line = line.strip()
        if stripped_line.startswith("#") or not stripped_line:
            continue
        try:
            key, value = stripped_line.split("=", 1)
        except ValueError as e:
            msg = f"Invalid line in .env file: {line}"
            raise cappa.Exit(msg, code=1) from e
        result[key] = value
    return result


def get_updated(env_content: str, config: dict, *, keep_original=False, keep_whitespace=False) -> str:
    content_list = env_content.split("\n")
    content_dict = {line.split("=")[0]: line for line in content_list if "=" in line}
    new_content_list = content_list.copy()

    for key, value in config.items():
        line = content_dict.get(key)
        if line is not None:
            index = new_content_list.index(line)
            if not keep_original:
                new_content_list[index] = f"{key}={value}"
        else:
            new_content_list.append(f"{key}={value}")

    if not keep_whitespace:
        new_content_list = [line.strip() for line in new_content_list if line.strip()]

    return "\n".join(new_content_list)
