from __future__ import annotations

import secrets
from pathlib import Path
from typing import Annotated

import cappa
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

        config = self.get_config(dotenv_content, dotenv_template_content)

        if self.fill_missing:
            for key, value in config.items():
                if not value:
                    config[key.upper()] = Prompt.ask(f"{key}")
            postgres_user = Prompt.ask("Postgres user", default="postgres")
            postgres_password = Prompt.ask("Postgres password", default="postgres")
            config["DATABASE_URL"] = f"postgres://{postgres_user}:{postgres_password}@127.0.0.1:5432/{project_name}"

        dotenv_content = get_updated(dotenv_content, config)
        if self.print_env:
            rich_print(dotenv_content)
            return

        dotenv_file.touch(exist_ok=True)
        dotenv_file.write_text(dotenv_content)

        dotenv_template_content = get_updated(
            dotenv_template_content, {key: "" for key in config}, keep_original=True, keep_whitespace=True
        )
        dotenv_template_file.touch(exist_ok=True)
        dotenv_template_file.write_text(dotenv_template_content)

        rich_print(f"[green] {dotenv_file} and {dotenv_template_file} synchronised [/green]")

    def get_config(self, env_content: str, env_template_content: str) -> dict:
        default_values = {
            "DJANGO_DEBUG": True,
            "DJANGO_ENV": "dev",
            "DJANGO_SECRET_KEY": secrets.token_urlsafe(64),
            "DJANGO_ALLOWED_HOSTS": "*",
            "DATABASE_URL": "sqlite:///db.sqlite3",
            "DJANGO_SUPERUSER_EMAIL": "",
            "DJANGO_SUPERUSER_PASSWORD": "",
        }
        return {
            **parse(env_template_content),
            **default_values,
            **parse(env_content),
        }


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
