The CLI
=======

The falco CLI is included with the package installation. It provides a set of commands that I hope will be useful to you throughout the
lifecycle of your project, from project setup to deployment.

.. note::

    If you encounter any issues or unexpected behavior with the CLI, please report it on
    `GitHub <https://github.com/tobi-de/falco/discussions>`_.

.. admonition:: Install the cli
   :class: dropdown hint

   .. code:: console

      $ pip install falco-cli


The entrypoint for the CLI is the ``falco`` command. It is used to run the commands that are available to you.

.. figure:: ../images/falco.svg


.. toctree::
   :hidden:

   start_project
   crud
   htmx
   work
   rm_migrations
   sync_dotenv
   make_superuser
