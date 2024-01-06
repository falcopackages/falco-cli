The CLI
=======

The falco CLI is included with the package installation. It provides a set of commands that I hope will be useful to you throughout the
lifecycle of your project, from project setup to deployment.

.. note::

    If you encounter any issues or unexpected behavior with the CLI, please report it on
    `GitHub <https://github.com/tobi-de/falco/discussions>`_.


The entrypoint for the CLI is the ``falco`` command. It is used to run every other subcommands.
Most of the commands here depends on the ``manage.py`` file, so make sur to run them at the root of
your django project.

.. important::

    There is a current issue where some commands, which depend on your Django project environment to work, such as the ``work`` or the
    ``crud`` commands, might occasionally fail to run. The exact cause of this issue is not entirely clear at the moment, and I've
    experienced it a few times myself. If you are running a project generated with the ``start-project`` command (which, for example,
    does not depend on your Django project environment), this issue should never occur. However, if it happens with other setups,
    try installing the ``falco-cli`` in the same virtual environment as your project. This should resolve the issue.

.. cappa:: falco.__main__.Falco

.. toctree::
   :hidden:

   start_project
   crud
   htmx
   work
   migrations
   sync_dotenv
   make_superuser
