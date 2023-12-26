Keep the .env and .env.template in sync
=======================================


.. cappa:: falco.commands.SyncDotenv


Any Django project created with the `start-project </guides/start_project.html>`_ command comes with a `.env.template` file. It serves as an example for the environment variables that
you need to fill in the `.env` file for your project to run. This command is a simple convenience that keeps the values in sync between the two files. It can be useful when you generate
a new project to create a `.env` file and when you add variables to the `.env` but forget to add them to the `.env.template`. You can even automate this process using a pre-commit hook
so that you never have to remember to keep your `.env.template` up to date.

**Example of pre-commit hook**

.. code:: yaml

  - repo: local
    hooks:
      - id: sync-dotenv
        name: sync-dotenv
        entry: hatch sync-dotenv
        language: system

When you run the ``sync-dotenv`` command, it performs the following steps:

#. It reads the values from the ``.env.template`` file, a set of default values (see below), and the ``.env`` file, in that order. If the same key is present in multiple sources, the value from the later source is used.
#. If the ``--fill-missing`` option is provided, it will prompt you to fill in any values that are currently empty.
#. It sorts the configuration keys alphabetically.
#. It empties the ``.env`` file and writes the new configuration values to it. Each key-value pair is written on a new line, with the format ``KEY=VALUE``.
#. It empties the ``.env.template`` file and writes the new configuration keys to it. If a key was originally present in the ``.env.template`` file, its value is preserved; otherwise, the value is left empty.


**Default Values**

The command uses the following default values:

- ``DJANGO_DEBUG``: ``True``
- ``DJANGO_SECRET_KEY``: A randomly generated secure token.
- ``DJANGO_ALLOWED_HOSTS``: ``*``
- ``DATABASE_URL``: ``postgres:///<project_name>``, where ``<project_name>`` is the name of the current directory.
- ``DJANGO_SUPERUSER_EMAIL``:
- ``DJANGO_SUPERUSER_PASSWORD``:

These values are used if they are not already specified in the ``.env`` or ``.env.template`` files.
