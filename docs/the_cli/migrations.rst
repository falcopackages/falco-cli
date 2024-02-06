:image: https://raw.githubusercontent.com/Tobi-De/falco/main/assets/og-image.jpg

Remove / Reset your migrations
==============================

.. important::
    Unless you know what you're doing, both of these commands should not be used once your project has gone live.
    In other words, they become essentially useless once real users start interacting with your application.

rm-migrations
-------------

.. cappa:: falco.commands.RmMigrations

It is a good idea to delete all migrations and recreate them from scratch when deploying your django project for the fist time.
This ensures a clean base without any remnants of testing or experimentation from the initial development phase. Even during development,
when exploring new ideas, it is often necessary to delete all migrations and start over. This command is designed for these scenarios,
as it deletes all migrations in your project.
The command checks the debug value of your project using the ``manage.py`` file. If the debug value is set to ``False``, the command will fail.
It takes an optional argument, ``apps_dir``, which specifies the directory containing your apps. If no argument is provided, it assumes that the apps
directory has the same name as the current parent directory. For example, if your project is named ``my_awesome_project``, the command will assume that
the apps directory is a subdirectory with the same name, i.e., ``my_awesome_project/my_awesome_project``. This is the default project layout created
by the `falco startproject </the_cli/start_project.html>`_ command.

**Example**

.. code:: shell

   falco rm-migrations
   # or
   falco rm-migrations my_apps_dir

.. warning::

   This command will delete all your migrations files, be sure to commit your changes before running this command.

After deleting all your migrations, your next step might likely be to reset your database using a command like ``reset-db``
from `django-extensions <https://django-extensions.readthedocs.io/en/latest/>`_. However, if you want to preserve your data,
then the following command might be a better option than running ``rm-migrations`` altogether.

reset-migrations
----------------

.. cappa:: falco.commands.ResetMigrations

This command works exactly like the ``rm-migration`` command but goes a bit further. Here's how it works:

1. First, it runs ``falco rm-migrations``.
2. Then, it clears your django migrations table:

        .. code-block:: python

            from django.db import connection

            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM django_migrations")

3. Next, it runs ``python manage.py makemigrations`` to recreate migrations.
4. Lastly, it executes ``python manage.py migrate --fake`` add the new migrations to the migrations table so that your migrations are in sync with the current database schema state.

The `migrate fake <https://docs.djangoproject.com/en/5.0/ref/django-admin/#cmdoption-migrate-fake>`_ command apply migrations without running
the actual SQL.
Since the ``reset-migrations`` depends on the ``rm-migrations`` command, it performs the same checks: it checks your Django ``DEBUG`` value and your Git
repo needs to be in a clean state unless you use the ``--skip-git-check`` option.

This command allows you to restore your migrations to their initial state without losing any existing data.
