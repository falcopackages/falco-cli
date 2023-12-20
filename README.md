<p align="center">
  <a href="https://falco.oluwatobi.dev/"><img src="https://raw.githubusercontent.com/Tobi-De/falco/main/assets/falco-logo.svg" alt="falco logo" height="200"/></a>
</p>

<h1 align="center">
  <a href="https://www.django-unicorn.com/">Falco</a>
  <p>The toolkit for a better django development experience</p>
</h1>

[![documentation](https://github.com/Tobi-De/falco/actions/workflows/documentation.yml/badge.svg)](https://github.com/Tobi-De/falco/actions/workflows/documentation.yml)
[![Continous Integration - Testing](https://github.com/Tobi-De/falco/actions/workflows/ci.yml/badge.svg)](https://github.com/Tobi-De/falco/actions/workflows/ci.yml)
[![pypi](https://badge.fury.io/py/falco-cli.svg)](https://pypi.org/project/falco-cli/)
[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/Tobi-De/falco/blob/main/LICENSE)

> [!WARNING]
> This is a work in progress (WIP), this is also [fuzzy-couscous](https://github.com/Tobi-De/fuzzy-couscous) new cooler brother.

<!-- start-docs -->

Intro here....

<!-- [![Read the full documentation](https://img.shields.io/badge/Read%20The%20full%20Documentation-blue?style=for-the-badge&logo=ReadTheDocs)](https://falco.oluwatobi.dev) -->


## The CLI

This is a set of commands to help you throughout the lifecycle of your django project development, from bootstrapping a new project using modern tools like [htmx](https://htmx.org), [hatch](https://github.com/pypa/hatch), [tailwindcss](https://tailwindcss.com/), to generating CRUD views for your models and a few utilities that might help during deployment.

<!-- [![The CLI full documentation](https://img.shields.io/badge/Read%20The%20CLI%20Documentation-blue?style=for-the-badge&logo=ReadTheDocs)](https://falco.oluwatobi.dev/the_cli/) -->


```sh
pip install falco-cli
```

- `start-project`: Initialize a new django project the falco way.
- `crud`: Generate CRUD (Create, Read, Update, Delete) views for a model.
- `work`: Run your whole django projects in one command.
- `htmx`: Download the latest version (if no version is specified) of htmx.
- `htmx-ext`: Download one of htmx extensions.
- `sync-dotenv`: Synchronize the `.env` file with the `.env.template` file.
- `rm-migrations`: Remove all migrations for the specified applications directory, intended only for development.


## The guides

> [!NOTE]
> These are currently a work in progress. Most of them are half-written or not written at all. I hope
> to get them in a usable state by the end of january 2024.

If you don't find any use of the CLI, I hope you will in these guides. This is a collection of guides that address common issues in web development, specifically tailored to Django. Each guide provides solutions, patterns, and approaches that are relevant to Django projects. It is similar to the [Django topic guides](https://docs.djangoproject.com/en/5.0/topics/), but instead of focusing on components of the framework like `forms`, `models`, `views`, etc., it focuses on more general topics like `task queues`, `deployment`, `realtime`, etc.

<!--
[![The full Guides](https://img.shields.io/badge/Read%20The%20Full%20Guides-blue?style=for-the-badge&logo=ReadTheDocs)](https://falco.oluwatobi.dev/guides/) -->


<!-- GUIDES-LIST:START -->
- [Optimizing Database Access](https://falco.oluwatobi.dev/guides/optimizing_database_access.html)
- [Dynamic Model Schema](https://falco.oluwatobi.dev/guides/dynamic_model_schema.html)
- [Use Sqlite in production](https://falco.oluwatobi.dev/guides/use_sqlite_in_production.html)
- [Bussiness logic in django](https://falco.oluwatobi.dev/guides/avoiding_god_models.html)
- [Managing Multitenancy in Django](https://falco.oluwatobi.dev/guides/multitenancy.html)
- [Writing documentation](https://falco.oluwatobi.dev/guides/writing_documentation.html)
- [Database Tips: Backup, Scaling, Triggers, and More](https://falco.oluwatobi.dev/guides/database_tips.html)
- [Async Coding in Django](https://falco.oluwatobi.dev/guides/writting_async_code.html)
- [Realtime in Django: Websockets, SSE, Polling](https://falco.oluwatobi.dev/guides/realtime.html)
- [Task Queues and Schedulers](https://falco.oluwatobi.dev/guides/task_queues_and_schedulers.html)
- [Interactive UX (User Experience) with HTMX](https://falco.oluwatobi.dev/guides/interactive_user_experience_with_htmx.html)
- [Running your project in a single container](https://falco.oluwatobi.dev/guides/running_project_in_a_container.html)
- [Deploy your project](https://falco.oluwatobi.dev/guides/deployment.html)
- [Permissions and authorizations](https://falco.oluwatobi.dev/guides/permissions_and_authorization.html)
- [Writing tests](https://falco.oluwatobi.dev/guides/writing_tests.html)
- [Logging and monitoring](https://falco.oluwatobi.dev/guides/logging_and_monitoring.html)
- [Tips and extra](https://falco.oluwatobi.dev/guides/tips_and_extra.html)
<!-- GUIDES-LIST:END -->

## Acknowledgements

Falco is inspired by (and borrows elements from) some excellent starter templates:

- [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django)
- [django-hatch-startproject](https://github.com/oliverandrich/django-hatch-startproject)
- [django-unicorn](https://github.com/adamghill/django-unicorn) (Inspiration for the logo)

<!-- end-docs -->
