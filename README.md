<p align="center">
  <a href="https://falco.oluwatobi.dev/"><img src="https://raw.githubusercontent.com/Tobi-De/falco/main/assets/falco-logo.svg" alt="falco logo" height="200"/></a>
</p>

<h1 align="center">
  <a href="https://falco.oluwatobi.dev">Falco</a>
  <p>An opinionated toolkit for a modern Django development experience</p>
</h1>

[![Documentation](https://github.com/Tobi-De/falco/actions/workflows/documentation.yml/badge.svg)](https://github.com/Tobi-De/falco/actions/workflows/documentation.yml)
[![Publish Python Package](https://github.com/Tobi-De/falco/actions/workflows/publish.yml/badge.svg)](https://github.com/Tobi-De/falco/actions/workflows/publish.yml)
[![pypi](https://badge.fury.io/py/falco-cli.svg)](https://pypi.org/project/falco-cli/)
[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/Tobi-De/falco/blob/main/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/falco-cli)](https://pypi.org/project/falco-cli/)
[![PyPI - Versions from Framework Classifiers](https://img.shields.io/pypi/frameworkversions/django/falco-cli)](https://pypi.org/project/falco-cli/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/falco-cli)](https://pypistats.org/packages/falco-cli)

> [!WARNING]
> The falco CLI isn't stable at the moment; stability is expected with the 1.0.0 release. I'm still making numerous changes quite frequently. If you're currently using it, remember to run `pip install --upgrade falco-cli` from time to time.

Falco is a Django-centric toolkit designed to enhance the development experience. The CLI offers commands for initiating new projects, generating simple CRUD views for rapid prototyping, and more. Additionally, it provides a collection of guides to address common issues in web development specifically tailored to Django.

<!-- [![Read the full documentation](https://img.shields.io/badge/Read%20The%20full%20Documentation-blue?style=for-the-badge&logo=ReadTheDocs)](https://falco.oluwatobi.dev) -->


## The CLI

This is a set of commands to help you throughout the lifecycle of your django project development, from bootstrapping a new project using modern tools like [htmx](https://htmx.org), [hatch](https://github.com/pypa/hatch), [tailwindcss](https://tailwindcss.com/), to generating CRUD views for your models and a few utilities that might help during deployment.

For a brief introduction to the user experience of the CLI, visit this [page](https://falco.oluwatobi.dev/the_cli/usage.html).
<!-- [![The CLI full documentation](https://img.shields.io/badge/Read%20The%20CLI%20Documentation-blue?style=for-the-badge&logo=ReadTheDocs)](https://falco.oluwatobi.dev/the_cli/) -->


```sh
pip install falco-cli
```

- [start-project](https://falco.oluwatobi.dev/the_cli/start_project.html): Initialize a new django project the falco way.
- [start-app](https://falco.oluwatobi.dev/the_cli/start_app.html): Initialize a new django app the falco way.
- [crud](https://falco.oluwatobi.dev/the_cli/crud.html): Generate CRUD (Create, Read, Update, Delete) views for a model.
- [install-crud-utils](https://falco.oluwatobi.dev/the_cli/crud.html#install-crud-utils): Install utils necessary for CRUD views.
- [work](https://falco.oluwatobi.dev/the_cli/work.html): Run all the services required to run your django project in parallel with a single command. (development only)
- [htmx](https://falco.oluwatobi.dev/the_cli/htmx.html): Download a local copy of the latest version of htmx.
- [htmx-ext](https://falco.oluwatobi.dev/the_cli/htmx.html#falco-htmx-ext): Download one of htmx extensions.
- [sync-dotenv](https://falco.oluwatobi.dev/the_cli/sync_dotenv.html): Synchronize the `.env` file with the `.env.template` file.
- [rm-migrations](https://falco.oluwatobi.dev/the_cli/migrations.html): Remove all migrations for the specified applications directory. (development only)
- [reset-migrations](https://falco.oluwatobi.dev/the_cli/migrations.html#reset-migrations): Delete and recreate all migrations. (development only)


## The guides

> [!NOTE]
> These are currently a work in progress. Most of them are half-written or not written at all. I hope
> to get them in a usable state ~~by the end of january 2024~~ as soon as I can. To receive updates [subscribe to this discussion](https://github.com/Tobi-De/falco/discussions/39) or
> follow me on [x](https://twitter.com/tobidegnon) or [mastodon](https://fosstodon.org/@tobide)

If you don't find any use of the CLI, I hope you will in these guides. This is a collection of guides that address common issues in web development, specifically tailored to Django. Each guide provides solutions, patterns, and approaches that are relevant to Django projects. It is similar to the [Django topic guides](https://docs.djangoproject.com/en/5.0/topics/), but instead of focusing on components of the framework like `forms`, `models`, `views`, etc., it focuses on more general topics like `task queues`, `deployment`, `realtime`, etc.

<!--
[![The full Guides](https://img.shields.io/badge/Read%20The%20Full%20Guides-blue?style=for-the-badge&logo=ReadTheDocs)](https://falco.oluwatobi.dev/guides/) -->


<!-- GUIDES-LIST:START -->
- [Interactive user interfaces](https://falco.oluwatobi.dev/guides/interactive_user_interfaces.html)
- [Task Queues and Schedulers](https://falco.oluwatobi.dev/guides/task_queues_and_schedulers.html)
- [Writing documentation](https://falco.oluwatobi.dev/guides/writing_documentation.html)
- [Writing tests](https://falco.oluwatobi.dev/guides/writing_tests.html)
- [Logging and monitoring](https://falco.oluwatobi.dev/guides/logging_and_monitoring.html)
- [The ultimate deployment guide](https://falco.oluwatobi.dev/guides/deployment.html)
- [Optimizing Database Access](https://falco.oluwatobi.dev/guides/optimizing_database_access.html)
- [Business logic in django](https://falco.oluwatobi.dev/guides/avoiding_god_models.html)
- [Dynamic Model Schema](https://falco.oluwatobi.dev/guides/dynamic_model_schema.html)
- [Realtime in Django: Websockets, SSE, Polling](https://falco.oluwatobi.dev/guides/realtime.html)
- [Permissions and authorizations](https://falco.oluwatobi.dev/guides/permissions_and_authorization.html)
- [Database Tips: Backup, Scaling, Triggers, and More](https://falco.oluwatobi.dev/guides/database_tips.html)
- [Managing Multi-tenancy in Django](https://falco.oluwatobi.dev/guides/multitenancy.html)
- [Async Coding in Django](https://falco.oluwatobi.dev/guides/writing_async_code.html)
- [Use Sqlite in production](https://falco.oluwatobi.dev/guides/use_sqlite_in_production.html)
- [Running your project in a single container](https://falco.oluwatobi.dev/guides/running_project_in_a_container.html)
- [Tips and extra](https://falco.oluwatobi.dev/guides/tips_and_extra.html)
<!-- GUIDES-LIST:END -->

## Acknowledgements

Falco is inspired by (and borrows elements from) some excellent open source projects:

- [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django)
- [fuzzy-couscous](https://github.com/Tobi-De/fuzzy-couscous) (predecessor of falco)
- [django-hatch-startproject](https://github.com/oliverandrich/django-hatch-startproject)
- [django-unicorn](https://github.com/adamghill/django-unicorn) (Inspiration for the logo)
- [neapolitan](https://github.com/carltongibson/neapolitan)
- [django-base-site](https://github.com/epicserve/django-base-site)
- [django-twc-project](https://github.com/westerveltco/django-twc-project)

## Contributors
<!-- contributors:start -->
Thanks to the following wonderful people [emoji key](https://allcontributors.org/docs/en/emoji-key) who have helped build `falco`.

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-6-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="http://oluwatobi.dev"><img src="https://avatars.githubusercontent.com/u/40334729?v=4?s=100" width="100px;" alt="Tobi DEGNON"/><br /><sub><b>Tobi DEGNON</b></sub></a><br /><a href="https://github.com/Tobi-De/falco/commits?author=Tobi-De" title="Code">💻</a> <a href="https://github.com/Tobi-De/falco/commits?author=Tobi-De" title="Documentation">📖</a> <a href="https://github.com/Tobi-De/falco/commits?author=Tobi-De" title="Tests">⚠️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/hammadarshad1"><img src="https://avatars.githubusercontent.com/u/45298916?v=4?s=100" width="100px;" alt="Muhammad Hammad"/><br /><sub><b>Muhammad Hammad</b></sub></a><br /><a href="#ideas-hammadarshad1" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mathiasag7"><img src="https://avatars.githubusercontent.com/u/50689712?v=4?s=100" width="100px;" alt="mathiasag7"/><br /><sub><b>mathiasag7</b></sub></a><br /><a href="https://github.com/Tobi-De/falco/commits?author=mathiasag7" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://mainlydata.kubadev.com"><img src="https://avatars.githubusercontent.com/u/403435?v=4?s=100" width="100px;" alt="Richard Shea"/><br /><sub><b>Richard Shea</b></sub></a><br /><a href="https://github.com/Tobi-De/falco/commits?author=shearichard" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://lexumsoft.com/"><img src="https://avatars.githubusercontent.com/u/96701299?v=4?s=100" width="100px;" alt="Waqar Khan"/><br /><sub><b>Waqar Khan</b></sub></a><br /><a href="https://github.com/Tobi-De/falco/commits?author=786raees" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/tissieres"><img src="https://avatars.githubusercontent.com/u/2410978?v=4?s=100" width="100px;" alt="tissieres"/><br /><sub><b>tissieres</b></sub></a><br /><a href="#financial-tissieres" title="Financial">💵</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
<!-- contributors:end -->
