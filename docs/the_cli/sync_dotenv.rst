:image: https://raw.githubusercontent.com/Tobi-De/falco/main/assets/og-image.jpg
:description: Keep your .env and .env.template files in sync.

Sync Dotenv files
=================


.. cappa:: falco.commands.SyncDotenv


Any Django project created with the `start-project </guides/start_project.html>`_ command comes with a ``.env.template`` file. It serves as an example for the environment variables that
you need to fill in the ``.env`` file for your project to run. This command is a simple convenience that keeps the values in sync between the two files. It can be useful when you generate
a new project to create a ``.env`` file and when you add variables to the ``.env`` and don't want to add them manually into the ``.env.template``. You can even automate this process using a pre-commit hook
so that you never have to remember to keep your ``.env.template`` up to date.

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


**Default values for production environments**

If you run the command with ``DEBUG=False`` it will try to fill in some default values for variables, such as the 
``SECRET_KEY``, ``DJANGO_SUPERUSER_EMAIL``, ``DJANGO_SUPERUSER_PASSWORD``, etc, where it makes sense.

.. code-block:: shell

  export DEBUG=False; falco sync-dotenv -p

You could, for example, pipe the result into another command to easily copy paste the config into your production environments.

.. code-block:: shell
  :caption: fill the missing values and copy it to the clipboard

  export DEBUG=False; falco sync-dotenv -p -f | clipcopy



