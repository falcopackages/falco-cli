:description: Things that does not deserve a full guide or I don’t know where to put them.

Tips and extra
==============

Things that does not deserve a full guide or I don’t know where to put them.


Understanding django Settings
-----------------------------

If there is a setting in ``settings.py`` or elsewhere that you don’t understand, go to the `official django settings reference page <https://docs.djangoproject.com/en/dev/ref/settings/>`__
and press Ctrl + F to search for it. I used the `django-production <https://github.com/lincolnloop/django-production>`__ package to configure the production settings which I then customized.
I have removed the package as a dependency, but I advise you to go and check for yourself what is available.

Local email testing
--------------------

https://github.com/axllent/mailpit


Lifecycle not signals
---------------------


Better use personal info fields
--------------------------------

The project also includes `django-improved-user <https://django-improved-user.readthedocs.io/en/latest/index.html>`__ which replaces the common ``first_name`` and ``last_name`` used for user details with ``full_name``
and the ``short_name`` fields. If you want to know the reasoning behind this, read the `project rationale <https://django-improved-user.readthedocs.io/en/latest/rationale.html>`__.
Currently, the latest version of ``django-improved-user`` that works without problems is an alpha version (v2.0a2). This can be annoying

Avoid huge apps for large projects
----------------------------------

Generate admin
--------------

https://django-extensions.readthedocs.io/en/latest/admin_generator.html

.. code-block:: bash

    python manage.py admin_generator your_app | tail -n +2 > your_project/your_app/admin.py

As a hatch script

.. code-block:: toml

    [tool.hatch.envs.default.scripts]
    admin = "python manage.py admin_generator {args} | tail -n +2 > your_project/{args}/admin.py"



Faster reload
-------------

https://github.com/reloadware/reloadium


Auto Fill forms
---------------

Fake filler


Book Recommendations
--------------------
