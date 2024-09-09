from pathlib import Path
from typing import cast
from typing import TypedDict

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack

import tomlkit


class FalcoConfig(TypedDict, total=False):
    revision: str
    blueprint: str
    skip: list[str]
    work: dict[str, str]
    htmx: str
    crud: "CRUDConfig"


class CRUDConfig(TypedDict):
    blueprints: str
    login_required: bool
    skip_git_check: bool
    always_migrate: bool


def parse_crud_config_from_pyproject(values: dict) -> dict:
    return {key.lower().replace("-", "_"): value for key, value in values.items()}


def parse_crud_config_to_pyproject(values: dict) -> dict:
    return {key.lower().replace("_", "-"): value for key, value in values.items()}


def write_falco_config(pyproject_path: Path, **kwargs: Unpack[TypedDict]) -> None:
    new_falco_config = kwargs
    new_crud_config = parse_crud_config_to_pyproject(new_falco_config.pop("crud", {}))

    # pyproject = tomlkit.parse(pyproject_path.read_text()) if pyproject_path.exists() else {}
    if pyproject_path.exists():  # noqa
        pyproject = tomlkit.parse(pyproject_path.read_text(encoding="utf-8"))
    else:
        pyproject = {}
    existing_falco_config = pyproject.get("tool", {}).get("falco", {})
    existing_crud_config = existing_falco_config.pop("crud", {})

    existing_crud_config.update(new_crud_config)
    existing_falco_config.update({**new_falco_config, "crud": existing_crud_config})

    tool = pyproject.get("tool", {})
    tool.update({"falco": existing_falco_config})
    pyproject["tool"] = tool
    pyproject_path.write_text(tomlkit.dumps(pyproject), encoding="utf-8")


def read_falco_config(pyproject_path: Path) -> FalcoConfig:
    pyproject = tomlkit.parse(pyproject_path.read_text(encoding="utf-8"))
    falco_config = pyproject.get("tool", {}).get("falco", {})
    crud_config = falco_config.pop("crud", {})
    crud_config = parse_crud_config_from_pyproject(crud_config)
    return cast(FalcoConfig, {**falco_config, "crud": crud_config})
