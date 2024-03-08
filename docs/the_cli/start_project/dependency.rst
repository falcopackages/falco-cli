:image: https://raw.githubusercontent.com/Tobi-De/falco/main/assets/og-image.jpg
:description: Virtualenv and dependencies management with a project generated with falco.

Virtualenv and dependencies
===========================

This is mainly handled using ``hatch``, ``hatch-pip-compile``, and the ``pyproject.toml`` file.

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

Read the hatch documentation on `environment <https://hatch.pypa.io/latest/environment/>`_ for more information on how to manage virtual environments.
Hatch can do a lot, including `managing Python installations <https://hatch.pypa.io/latest/cli/reference/#hatch-python>`_, but for the context of the project, these are the things you need to know.

.. admonition:: Specify a Python Version
   :class: dropdown note

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

The project comes with three environment configurations: ``default``, ``test``, and ``docs``.

- The ``default`` environment is activated when you run ``hatch shell``. It contains all the necessary requirements and some development tools.
- The ``test`` environment contains packages used for testing, such as ``pytest``, ``django-pytest``, etc.
- The ``docs`` environment is for documentation. It contains tools such as ``sphinx``, ``furo``, etc.

Each environment defines a scripts section with some scripts. To run a script, use the following command:

.. code-block:: bash

   hatch run <env>:<script>

The first time you run the script, Hatch automatically sets up and installs dependencies for the specified environment. 
You don't need to manage it manually. If the dependencies list has changed, Hatch will automatically install them the next 
time a command from that environment is run.

A requirements file for the environment is also created using `hatch-pip.compile <https://github.com/juftin/hatch-pip-compile>`_. For 
the default environment, the file will be located at the root of your project and named ``requirements.txt``. This is the file 
you would use to install the requirements in production. For other environments, the file is created in a 
``requirements`` folder with the name ``requirements-<env>.txt``.


Activate the virtual environment
********************************

To activate the default virtual environment, run:

.. code-block:: bash

   $ hatch shell

You don't need to activate your shell to run commands. When using ``hatch run``, dependencies will be automatically synced (installed or removed if necessary) and the command will be
executed in the appropriate virtual environment.

For instance, to run the Django development server, you can use the following command:

.. code-block:: bash

   $ hatch run python manage.py runserver

This will run your project in the default virtual environment.

Add / remove a new dependency
*****************************

The default virtual environment includes all the dependencies specified in the ``[project.dependencies]`` section of the ``pyproject.toml`` file.
To add a new dependency to your project, simply edit the ``pyproject.toml`` file and add it to the ``[project.dependencies]`` section.
The next time you run a command using hatch, such as ``hatch run python manage.py runserver``, hatch will automatically install the new dependency.
The process is the same for removing a dependency.

Scripts
*******

The ``pyproject.toml`` file in the project defines some convenient scripts for common commands in a Django project. The section looks something like this:

.. code-block:: toml

   [tool.hatch.envs.default.scripts]
   runserver = ["migrate", "python manage.py tailwind runserver {args}"]
   migrate = "python manage.py migrate {args}"
   makemigrations = "python manage.py makemigrations {args}"
   ...

To start the Django development server for example, you can use the command ``hatch run runserver``.

.. admonition:: Alias Hatch run
   :class: tip

   To make typing hatch commands faster, you can create an alias for ``hatch run``. For example, you can alias it as ``hr``. So,
   Instead of typing ``hatch run runserver``, you can simply use the alias ``hr runserver``. However, please note that if your system takes time to resolve the alias,
   it may impact your overall experience.

For development, I think this workflow should work quite well. Now, what happens when you need to deploy your app? You could install hatch on
the deploy target machine, but I prefer having a ``requirements.txt`` file that I can use to install dependencies on the deployment machine.
That's where ``hatch-pip-compile`` comes in.

.. admonition:: why hatch?
   :class: dropdown note

   Using hatch is a recent switch for me. Previously, I used `poetry <https://python-poetry.org/>`_ as my preferred tool. While poetry is still a great tool, I have chosen hatch for the following reasons:

   1. Backed by the **pypa** (Python Packaging Authority), hatch aligns with the efforts to solve packaging and tooling issues in the Python ecosystem. I believe that if the Python ecosystem ever manages to overcome these challenges, it will be because the pypa has reached a consensus, and I hope that hatch will be the chosen solution. We all hope to see a cargo-like tool for Python someday.

   2. Hatch now has the ability to install and manage Python versions, along with other existing features. This brings it closer to being the all-in-one tool that every Python developer needs.

   3. Hatch is PEP-friendly, making it compatible with other tools in the ecosystem. It adds minimal custom configuration to the ``pyproject.toml`` file and relies on existing standards for project information and dependencies.

   4. In terms of performance, hatch is faster compared to poetry. While poetry is generally not slow, there have been rare instances where it took 30 minutes to install requirements. I have experienced this a few times.


hatch-pip-compile
-----------------

The `hatch-pip-compile <https://github.com/juftin/hatch-pip-compile>`_ plugin is used with hatch to automatically generate a
requirements file (lock file) using `pip-tools <https://github.com/jazzband/pip-tools>`_. This file contains the dependencies of your hatch virtual environment with pinned versions.
The default setup generates a ``requirements.txt`` file that can be used for installing dependencies during deployment, as shown in the provided Dockerfile. However, you can customize the plugin to save
locks for all your environments. Refer to the `hatch-pip-compile documentation <https://github.com/juftin/hatch-pip-compile>`_ for more details.

Here is the current configuration in the ``pyproject.toml`` file relevant to hatch-pip-compile:

.. code-block:: toml
   :caption: pyproject.toml

   [tool.hatch.env]
   requires = [
   "hatch-pip-compile"
   ]

   [tool.hatch.envs.default]
   type = "pip-compile"
   # pip-compile-installer = "pip-sync"
   pip-compile-installer = "uv"
   pip-compile-resolver = "uv"
   ...

Thanks to `hatch-pip-compile <https://juftin.com/hatch-pip-compile/>`_, we can try `uv <https://github.com/astral-sh/uv>`_, which is, and I quote:

   An extremely fast Python package installer and resolver, written in Rust. Designed as a drop-in replacement for pip and pip-compile

   -- Official github

Needless to say, it does make a noticeable difference in speed. If you encounter any issues with ``uv``, comment out the two lines referencing it in the above
config, and uncomment the currently commented one.


Working without hatch
---------------------

You don't have to use Hatch if you don't want to. Thanks to Hatch being very PEP-friendly, you can use the ``pyproject.toml`` file with recent versions of
pip to install the main dependencies of the project. You won't be able to use the scripts (for that, you can use `peothepoet <https://github.com/nat-n/poethepoet>`_) or any other Hatch features,
but you may not need them.

Let's assume you want to use the classic ``venv``. Here's what the workflow would look like:

1. Remove any Hatch-related configuration from the pyproject.toml file, including anything starting with ``[tool.hatch]``. This step is optional and up to your choice.
2. Create a virtual environment using ``python -m venv venv``.
3. Activate the virtual environment using ``source venv/bin/activate``.
4. Install the dependencies using ``pip install -e .``. This command will install your project and its dependencies using the ``pyproject.toml`` file.

To add or remove dependencies, the process is the same. You edit the ``[project.dependencies]`` section of the pyproject.toml file and run ``pip install -e .``. You can complement
this workflow with `pip-tools <https://github.com/jazzband/pip-tools>`_ to generate a requirements file.




.. _hatch: https://hatch.pypa.io/latest/