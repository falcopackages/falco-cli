:description: Learn how to manage your Django migrations with Falco.

reset_migrations
================

.. exec_code::
    :language_output: shell

    # --- hide: start ---
    from falco.management.commands.crud import Command

    Command().print_help("manage.py", "reset_migrations")
    #hide:toggle

.. warning::
    Before running this command, make sure you have applied any pending migrations, ``makemigrations && migrate``. The idea is to reset the migrations while keeping the data. If your current database does not have up to date migrations, it will fail.


This command works exactly like the ``rm_migration`` command but goes a bit further. Here's how it works:

1. First, it runs ``rm_migrations``.
2. Then, it clears your django migrations table:

.. code-block:: python

    from django.db import connection

    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM django_migrations")

3. Next, it runs ``python -m myproject makemigrations`` to recreate migrations.
4. Lastly, it executes ``python -m myproject migrate --fake`` add the new migrations to the migrations table so that your migrations are in sync with the current database schema state.

The `migrate fake <https://docs.djangoproject.com/en/5.0/ref/django-admin/#cmdoption-migrate-fake>`_ command apply migrations without running
the actual SQL.
Since the ``reset_migrations`` depends on the ``rm_migrations`` command, it performs the same checks: it checks your Django ``DEBUG`` value and your Git
repo needs to be in a clean state unless you use the ``--skip-git-check`` option.
This command allows you to restore your migrations to their initial state without losing any existing data.
