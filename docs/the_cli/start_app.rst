:image: https://raw.githubusercontent.com/Tobi-De/falco/main/assets/og-image.jpg
:description: Start a new django app that's automatically registered to your installed apps.

Start Application
=================

.. cappa:: falco.commands.StartApp

This command executes Django's ``startapp``, along with a few additional tasks:

- It deletes the ``tests.py`` file. I never use a single test file when writing tests.
- It moves the newly created app to the ``apps_dir``. In the context of **Falco** projects, the ``apps_dir`` is a subdirectory in your root directory named after your project.
- It registers the new app in your settings under ``INSTALLED_APP``.
- It add a basic empty model to your ``models.py`` file.

These are tasks I always perform when generating a new app with Django. Now, I can reclaim those precious seconds I would have 
spent doing this manually.

