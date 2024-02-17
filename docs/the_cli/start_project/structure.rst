:image: https://raw.githubusercontent.com/Tobi-De/falco/main/assets/og-image.jpg
:description: Files and forlder structure of project generated with falco.


Project structure
=================

Let's go through overview of the folders that comes wizh





Now w'll go through more details about the structure, layouts and packages used for the project template and therefore available
in your generated project.


With this layout, your local apps reside in a subdirectory with the same name as your project. Every time you create a new app,
you should move it to that subdirectory and rename it (e.g., from ``myapp`` to ``myproject.myapp``) in the ``apps.py`` file.

.. admonition:: falco start-app
   :class: dropdown hint

   The ``falco start-app`` take care of moving th your app to the right place and registering it in your ``INSTALLED_APPS``

All your project configurations, settings, URLs, WSGI app file, etc., reside in the ``config`` folder.


Here is an overview of the complete file structure of a generated project:

.. figure:: ../../images/project-tree.svg