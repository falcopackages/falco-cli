:image: https://raw.githubusercontent.com/Tobi-De/falco/main/assets/og-image.jpg
:description: Files and forlder structure of project generated with falco.


Project Structure
=================

Let's go through the basics of the file structure and folders, We won't cover the entire file structure, just the essentials.

- ``.github``: Contains `GitHub Actions <https://docs.github.com/en/actions>`_ workflows and `Dependabot <https://docs.github.com/en/code-security/supply-chain-security/keeping-your-dependencies-updated-automatically>`_ configurations. More details on this can be found in the `packages and tools </the_cli/start_project/packages.html#continuous-integration>`_ section.
- ``docs``: Documentation for your project generated with `Sphinx <https://www.sphinx-doc.org/en/master/>`_. More details on this can be found in the `packages and tools </the_cli/start_project/packages.html#documentation>`_ section.
- ``project_dir``: The core of your Django project. It contains all the essentials of your Django project: ``settings``, ``root urls``, ``applications``, ``templates``, and ``static`` files. Your apps will be located here when using the `start-app </the_cli/start_app.html>`_ command that comes with Falco.
- ``project_dir/__main__.py``: This file is the entry point of your project. It is mainly meant for production and building the binary of your project. More details on this can be found in the `deployment </the_cli/start_project/deploy.html>`_ section.
- ``deploy``: Contains all tools and configuration files related to deployment, such as Dockerfile, s6-overlay, etc. You can also add your Nginx and systemd files here if you use those. The goal is to keep all files related to deployment in the same place and sync them with the server when needed. This way, it is easier to keep track of all configurations involved in deployment.
- ``justfile``: A file that contains the commands you can run with the ``just`` command. It also serves as a convenient way to document frequently used commands in your project.
- ``pyproject.toml``: A file that contains the project metadata, dependencies, and some tool configurations. More details on this can be found in the `dependency </the_cli/start_project/dependency.html>`_ section.
- ``CHANGELOG.md``: A file that contains the project changes. This file will automatically be filled using ``git-cliff``. More details on this can be found in the `package and tools </the_cli/start_project/packages.html#project-versioning>`_ section.
- ``playground.ipynb``: This is meant as a playground for writing ORM Django queries. More details on this can be found in the `packages and tools </the_cli/start_project/packages.html#dj-notebook>`_ section.
- ``.pre-commit-config.yaml``: A file that contains the `pre-commit <https://pre-commit.com/>`_ configurations. When configured, the hooks defined inside will run before any commits and will perform some linting and code formatting.






