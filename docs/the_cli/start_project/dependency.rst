:description: Virtualenv and dependencies management with a project generated with falco.

Python Environment
==================

This is mainly handled using ``hatch``, ``hatch-pip-compile``, and the ``pyproject.toml`` file.
Additionally, there is a ``.github/dependabot.yml`` file. It is a config file for `Dependabot <https://github.com/dependabot>`_ that is configured to
check weekly for dependency upgrades in your requirements files and create pull requests for them.

.. admonition:: Replacing hatch
   :class: tip dropdown

   The project is set up in a way that the underlying environment and dependencies tool should be quite transparent to you. Most of the commands you will run
   will happen through the ``just`` script runner, which will automatically run the command in the appropriate virtual environment.
    
   If I ever change the underlying tool to use ``uv`` or just plain old ``pip``, for example, it should not affect your workflow. You can even do it yourself 
   if you feel like it, the main thing you'll have to do is update the ``justfile``.

The pyproject.toml File
-----------------------

The ``pyproject.toml`` file is a Python standard introduced to unify and simplify Python project packaging and configurations. It was introduced by `PEP 518 <https://www.python.org/dev/peps/pep-0518/>`_ and `PEP 621 <https://www.python.org/dev/peps/pep-0621/>`_.
For more details, check out the `complete specifications <https://packaging.python.org/en/latest/specifications/pyproject-toml/#pyproject-toml-spec>`_.
Many tools in the Python ecosystem, including hatch, support it, and it seems that this is what the Python ecosystem has settled on for the future.

Hatch
-----

The project is set up to use hatch_ for virtual environment management and dependencies management.

   "Hatch is a modern, extensible Python project manager."

   -- Official hatch documentation


.. admonition:: why hatch?
   :class: dropdown note

   Using hatch is a recent switch for me. Previously, I used `poetry <https://python-poetry.org/>`_ as my preferred tool. While poetry is still a great tool, I have chosen hatch for the following reasons:

   1. Backed by the **pypa** (Python Packaging Authority), hatch aligns with the efforts to solve packaging and tooling issues in the Python ecosystem. I believe that if the Python ecosystem ever manages to overcome these challenges, it will be because the pypa has reached a consensus, and I hope that hatch will be the chosen solution. We all hope to see a cargo-like tool for Python someday.

   2. Hatch now has the ability to install and manage Python versions, along with other existing features. This brings it closer to being the all-in-one tool that every Python developer needs.

   3. Hatch is PEP-friendly, making it compatible with other tools in the ecosystem. It adds minimal custom configuration to the ``pyproject.toml`` file and relies on existing standards for project information and dependencies.

   4. In terms of performance, hatch is faster compared to poetry. While poetry is generally not slow, there have been rare instances where it took 30 minutes to install requirements. I have experienced this a few times.


Read the hatch documentation on `environment <https://hatch.pypa.io/latest/environment/>`_ for more information on how to manage virtual environments.
Hatch can do a lot, including `managing Python installations <https://hatch.pypa.io/latest/cli/reference/#hatch-python>`_, but for the context of the project, these are the things you need to know.

.. admonition:: Specify a Python Version
   :class: dropdown tip

   If you have multiple Python interpreter versions installed on your computer, you can specify the specific version you want to use for a project
   by setting the ``python`` option in your default environment. Every other environment inherits from the default, so they will use the same version.

   .. code-block:: toml
      :caption: pyproject.toml

      [tool.hatch.envs.default]
      python = "3.12"
      ...

   More information on this can be found `here <https://hatch.pypa.io/latest/plugins/environment/virtual/#pyprojecttoml>`_.


Environments
************

The project comes with three environment configurations: ``default``, ``dev``, and ``docs``.

- The ``default`` environment is activated when you run ``hatch shell``. It is the default environment made available by Hatch and contains all the required dependencies for your project to run in production.
- The ``dev`` environment contains packages used for development and testing, such as ``django-debug-toolbar``, ``pytest``, ``django-pytest``, etc.
- The ``docs`` environment is for documentation. It contains tools such as ``sphinx``, ``furo``, etc.

.. admonition:: Install all dependencies
   :class: dropdown tip

   Running ``just bootstrap`` will create all three environments and install the dependencies for each.

Although ``hatch`` comes with an integrated script runner, the project uses `just <https://just.systems/>`_ as the script runner. The main reason is that it is a more universal solution (not limited to the Python ecosystem) and
I find it more flexible. Paired with the `scripts-to-rule-them-all <https://github.com/github/scripts-to-rule-them-all>`_ pattern, it's an efficient way to standardize a set of commands
(``setup``, ``server``, ``console``, etc.) across all your projects, whether they are Django, Python, or something else. This way, you don't need to remember a different set of commands for each project.

To see all available scripts or `recipes` as ``just`` calls them, you can run:

.. code-block:: bash

   $ just

The primary environment you'll use during development is the ``dev`` environment. To run a command, you can either run ``just run`` or ``hatch --env dev run``. The first command is basically an alias for the second.

**Examples**

.. code-block:: bash

   $ just run python # launch the Python shell
   $ just run python manage.py dbshell # launch the database shell

There are aliases for most Django commands, such as ``just server`` to run the development server, ``just migrate`` to apply migrations, ``just createsuperuser`` to create a superuser, etc.
. For any other commands that aren't explicitly aliased, you can run ``just dj <command>`` to run the command in the Django context.

Activate the virtual environment
********************************

To activate an environment for the current shell, run ``hatch shell <env_name>``, so ``hatch shell dev`` will activate the ``dev`` environment. If no specific environment name is provided, the default environment is activated.

.. admonition:: Get the path of the dev environment
   :class: dropdown tip

   You can get the full path of the dev environment with ``just env-path`` or ``just env-path dev``. This can be useful to specify the interpreter in VSCode or PyCharm, for example.

You don't need to activate your shell to run commands. When running a just script, dependencies will be automatically synced (installed or removed if necessary), since it uses Hatch underneath, and
the command will be executed in the appropriate virtual environment.


Add / remove a new dependency
*****************************

To add or remove a dependency, edit the ``[project.dependencies]`` section of the ``pyproject.toml`` file for a dependency that should be included in all environments and is needed in production.
Alternatively, edit the ``dependencies`` key of ``[tool.hatch.envs.dev]`` or the ``extra-dependencies`` key of ``[tool.hatch.envs.docs]`` to add a development or documentation-only dependency, respectively.
The next time you run a command using ``just``, such as ``just server``, Hatch (used underneath by the just script) will automatically install the new dependency.

.. code-block:: shell
    :caption: Immediately sync dependencies

    just install

For development, I think this workflow should work quite well. Now, what happens when you need to deploy your app? You could install Hatch on the deployment target machine, but I
prefer having a ``requirements.txt`` file that I can use to install dependencies on the deployment machine. That's where ``hatch-pip-compile`` comes in.


hatch-pip-compile
-----------------

The `hatch-pip-compile <https://github.com/juftin/hatch-pip-compile>`_ plugin is used with hatch to automatically generate a
requirements file (lock file) using `pip-tools <https://github.com/jazzband/pip-tools>`_. This file contains the dependencies of your hatch virtual environment with pinned versions.
The default setup generates a ``requirements.txt`` file that can be used for installing dependencies during deployment, as shown in the provided Dockerfile, a ``requirements-dev.txt``
file for development dependencies, and a ``docs/requirements.txt`` file for documentation dependencies.

Here is the current configuration in the ``pyproject.toml`` file relevant to hatch-pip-compile:

.. code-block:: toml
   :caption: pyproject.toml

   [tool.hatch.env]
   requires = [
      "hatch-pip-compile>=1.11.2"
   ]

   [tool.hatch.envs.default]
   type = "pip-compile"
   pip-compile-constraint = "default"
   pip-compile-installer = "uv"
   pip-compile-resolver = "uv"
   lock-filename = "requirements.txt"
   ...

You can specify the tool for dependency installation using `hatch-pip-compile <https://juftin.com/hatch-pip-compile/>`_. By default, it is configured to use `uv <https://github.com/astral-sh/uv>`_, which is, and I quote:

   An extremely fast Python package installer and resolver, written in Rust. Designed as a drop-in replacement for pip and pip-compile

   -- Official github

Needless to say, it does make a noticeable difference in speed. If you encounter any issues with ``uv``, you can easily switch back to pip by updating the configurations as below:

.. code-block:: toml
   :caption: pyproject.toml

   [tool.hatch.envs.default]
   type = "pip-compile"
   pip-compile-constraint = "default"
   pip-compile-installer = "pip"
   pip-compile-resolver = "pip-compile"
   lock-filename = "requirements.txt"
   ...


.. _hatch: https://hatch.pypa.io/latest/
