:description:

Make a superuser from pre-configured settings
=============================================

.. cappa:: falco.commands.MakeSuperUser

This command is designed for convenience. It allows you to set up a superuser with pre-configured settings,
eliminating the need to enter any input. Please note that this command only works when authentication via **email** is configured, not
the default **username** authentication in Django. This applies to projects generated using the `start-project </the_cli/start_project>`_ command.
The two required settings are:

.. code-block:: python
    :caption: settings.py

    SUPERUSER_EMAIL = env('SUPERUSER_EMAIL')
    SUPERUSER_PASSWORD = env('SUPERUSER_PASSWORD')

This was previously a management command shipped with the starter project. If you prefer or would like to make changes to the code,
it is available `here <https://github.com/Tobi-De/fuzzy-couscous/blob/main/templates/project_name/project_name/core/management/commands/makesuperuser.py>`_.
