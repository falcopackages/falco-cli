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

.. cappa:: falco_cli.__main__.Falco

.. toctree::
   :hidden:

   usage
   start_project/index
   start_app
   crud
   htmx
   work
   migrations
   sync_dotenv
