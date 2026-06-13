:description: Remove all migrations in all applications.

rm_migrations
=============

.. exec_code::
    :language_output: shell

    # --- hide: start ---
    from falco.management.commands.crud import Command

    Command().print_help("manage.py", "rm_migrations")
    #hide:toggle

.. warning::
   This command will delete all your migrations files, be sure to commit your changes before running this command.


It is a good idea to delete all migrations and recreate them from scratch when deploying your django project for the first time.
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

After deleting all your migrations, your next step might likely be to reset your database using a command like ``reset-db``
from `django-extensions <https://django-extensions.readthedocs.io/en/latest/>`_. However, if you want to preserve your data,
then the following command might be a better option than running ``rm-migrations`` altogether.
