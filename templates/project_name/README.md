# {{ project_name }}

[![falco](https://img.shields.io/badge/built%20with-falco-success)](https://github.com/Tobi-De/falco)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)

## Prerequisites

- `Python 3.10+`
- `Poetry 1.2+`
- `Postgresql 10+`

## Development

### Create a new virtual environment

```shell
poetry shell
```
### Install dependencies

```shell
poetry install
```

### Install pre-commit

```shell
pre-commit install
```

### Run the django development server

```
poe r
```

[poethepoet](https://github.com/nat-n/poethepoet) is the task runner used here. To see all available commands read
 the `[tool.poe.tasks]`section of the `pyproject.toml` file or run `poe -h` to see the help page.
