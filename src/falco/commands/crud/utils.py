import importlib
import subprocess
from pathlib import Path

import cappa
from falco.utils import simple_progress
from jinja2 import Template


IMPORT_START_COMMENT = "# IMPORTS:START"
IMPORT_END_COMMENT = "# IMPORTS:END"
CODE_START_COMMENT = "# CODE:START"
CODE_END_COMMENT = "# CODE:END"


def render_to_string(template_content: str, context: dict):
    return Template(template_content).render(**context)


def get_crud_blueprints_path() -> Path:
    package = importlib.util.find_spec("falco")
    if package is None:
        raise cappa.Exit("The falco base install path could not be found.", code=1)
    return Path(package.submodule_search_locations[0]) / "crud"


@simple_progress("Running python formatters")
def run_python_formatters(filepath: str | Path):
    autoflake = [
        "autoflake",
        "--in-place",
        "--remove-all-unused-imports",
        filepath,
    ]
    black = ["black", filepath]
    isort = ["isort", filepath]
    subprocess.run(autoflake, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    subprocess.run(isort, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    subprocess.run(black, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)


@simple_progress("Running html formatters")
def run_html_formatters(filepath: str | Path):
    djlint = ["djlint", filepath, "--reformat"]
    subprocess.run(djlint, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)


def extract_python_file_templates(file_content: str) -> tuple[str, str]:
    imports_template = extract_content_from(file_content, IMPORT_START_COMMENT, IMPORT_END_COMMENT)
    code_template = extract_content_from(file_content, CODE_START_COMMENT, CODE_END_COMMENT)
    return imports_template, code_template


def extract_content_from(text: str, start_comment: str, end_comment: str):
    start_index = text.find(start_comment) + len(start_comment)
    end_index = text.find(end_comment)
    return text[start_index:end_index]
