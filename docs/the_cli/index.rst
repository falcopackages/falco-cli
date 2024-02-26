:image: https://raw.githubusercontent.com/Tobi-De/falco/main/assets/og-image.jpg
:description: A cli for faster prototyping of django projects.

The CLI
=======

The falco CLI is included with the package installation. It provides a set of commands that I hope will be useful to you throughout the
lifecycle of your project, from project setup to deployment.

.. note::

    If you encounter any issues or unexpected behavior with the CLI, please report it on
    `GitHub <https://github.com/tobi-de/falco/discussions>`_.


The entrypoint for the CLI is the ``falco`` command. It is used to execute all other subcommands.
Most of these commands rely on the presence of the ``manage.py`` file, so ensure that you run them from the root directory of your Django project.
Additionally, these commands require acces to your virtual environment, so make sure to activate it before executing any command.


.. important::

    There is a known issue where certain commands, which depend on your Django project environment to work, such as the ``work`` or the
    ``crud`` commands, might occasionally fail to run. The exact cause of this issue is not entirely clear at the moment, and I've
    experienced it a few times myself. The simplest solution for now is to install the ``falco-cli`` in the same virtual environment as your project.
    This should resolve the issue.

.. cappa:: falco.__main__.Falco

.. toctree::
   :hidden:

   usage
   start_project
   start_app
   crud
   htmx
   work
   migrations
   sync_dotenv
