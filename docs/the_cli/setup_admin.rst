:image: https://raw.githubusercontent.com/Tobi-De/falco/main/assets/falco-logo.svg
:description: Create a django admin user from pre-configured settings.

Setup admin user
================

.. cappa:: falco.commands.SetupAdmin

This command is designed for convenience. It allows you to set up a superuser with pre-configured settings,
eliminating the need to enter any input. Here's how it works: it reads all the settings that start with ``SUPERUSER_``, such as
``SUPERUSER_EMAIL`` or ``SUPERUSER_USERNAME``, and uses these settings to create a superuser. The only required setting is
``SUPERUSER_PASSWORD``. This makes it easier to add additional values, especially when using a highly customized ``User`` model.
The part after the ``SUPERUSER_`` prefix in the settings is used as an argument for the ``User.objects.create_superuser`` method.
For example, if you add a setting called ``SUPERUSER_FULL_NAME``, it will be passed as the ``full_name`` argument to the ``create_superuser`` method.

**Example of settings**

Here is the default configuration that is shipped with the starter project.

.. code-block:: python
    :caption: settings.py

    SUPERUSER_EMAIL = env('SUPERUSER_EMAIL')
    SUPERUSER_PASSWORD = env('SUPERUSER_PASSWORD')

This was previously a management command shipped with the starter project. If you prefer or would like to make changes to the code,
it is available `here <https://github.com/Tobi-De/fuzzy-couscous/blob/main/templates/project_name/project_name/core/management/commands/makesuperuser.py>`_.
