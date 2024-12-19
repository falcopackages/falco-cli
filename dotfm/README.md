# dotfm

[![falco](https://img.shields.io/badge/built%20with-falco-success)](https://github.com/Tobi-De/falco)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)

## Prerequisites

- `Python 3.11+`
- [hatch 1.9.1+](https://hatch.pypa.io/latest/)
- [just](https://github.com/casey/just)

## Development

### Setup project

Ensure that the Python version specified in your `.pre-commit-config.yaml` file aligns with the Python in your virtual environment.
Hatch can [manage your python installation](https://hatch.pypa.io/latest/tutorials/python/manage/) if needed.

```shell
just setup
```
Read the content of the justfile to understand what this command does. Essentially, it sets up your virtual environment, 
installs the dependencies, runs migrations, and creates a superuser with the credentials `admin@localhost` (email) and `admin` (password).

### Run the django development server

```shell
just server
```

> [!TIP]
> Run `just` to see all available commands.
