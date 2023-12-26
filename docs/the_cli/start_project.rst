:description: start a new django project ready for your next saas idea.

Start project
=============

.. cappa:: falco.commands.StartProject

Initialize a new Django project. This template makes several assumptions; we'll go through the most important choices I made below.
I'll list some alternatives below in case you don't agree with my choices. But even if you choose to use an alternative, most commands
can still be useful to you, and the `guides </guides/index.html>`__ are not particularly tied to the generated project. So, even with another template, **Falco**
can still bring you value.


.. note::

   The **authors** key of the ``[tool.project]`` section in the ``pyproject.toml`` is set using your git global user
   configuration. If you haven't set it yet, `see this page <https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup#_your_identity>`_.



Features
--------

- Django 4+
- Python 3.10+
- Frontend: `htmx <https://htmx.org/>`_
- Frontend CSS: `tailwindcss <https://tailwindcss.com/>`_ via `django-tailwind-cli <https://github.com/oliverandrich/django-tailwind-cli>`_
- Template fragment with `django-template-partials <https://github.com/carltongibson/django-template-partials>`_
- Secure production settings, https only.
- Settings using `django-environ <https://github.com/joke2k/django-environ>`_
- Login / signup via `django-allauth <https://github.com/pennersr/django-allauth>`_
- Login using email instead of username
- Automatically reload your browser in development via `django-browser-reload <https://github.com/adamchainz/django-browser-reload>`_
- Better development experience with `django-fastdev <https://github.com/boxed/django-fastdev>`_
- `Amazon SES <https://aws.amazon.com/ses/?nc1=h_ls>`_ for production email via `Anymail <https://github.com/anymail/django-anymail>`_
- `Docker <https://www.docker.com/>`_ ready for production
- Optional production cache settings using the ``CACHE_URL`` or ``REDIS_URL`` environment variables.
- `Sentry <https://sentry.io/welcome/>`_ for performance/error monitoring
- Serve static files with `Whitenoise <https://whitenoise.evans.io/en/latest/>`_
- Default integration with `pre-commit <https://github.com/pre-commit/pre-commit>`_ for identifying simple issues before submission to code review
- Dependency management using `hatch <https://github.com/pypa/hatch>`_
- Playground file for local testing with `dj-notebook <https://github.com/pydanny/dj-notebook>`_.

.. tip::

   If you are using a jetbrains IDE, there is an extension that add support for htmx, you can find it `here <https://plugins.jetbrains.com/plugin/20588-htmx-support>`_.
   If you use `alpinejs <https://alpinejs.dev/>`_ there is also for it via `this extension <https://plugins.jetbrains.com/plugin/15251-alpine-js-support>`_.


Project Structure
-----------------

Now w'll go through more details about the structure, layouts and packages used for the project template and therefore available
in your generated project.


.. figure:: ../images/project-tree.svg


Login via email instead of username
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

I completely removed the ``username`` field from the ``User`` model and replaced it with the ``email`` field as the user unique identifier.
This ``email`` field is what I configured as the login field via `django-allauth <https://github.com/pennersr/django-allauth>`__. More often then not when I create a new django project
I need to use something other than the ``username`` field provided by django as the unique identifier of the user, and the ``username`` field
just becomes an annoyance to deal with. It is also more common nowadays for modern web and mobile applications to rely on a unique identifier
such as an email address or phone number instead of a username.

to deal with when updating dependencies, you can get the same result as I just described with the django-authtools package.

https://gdpr.eu/compliance/

.. admonition:: Don’t ask for what you don’t need
   :class: note

   Make sure you need ``first_name`` - ``last_name`` or ``short_name`` - ``full_name`` before asking your users for this information.

::

   !!! Quote "[rezaid.co.uk](https://rezaid.co.uk/app-website-gdpr-compliant/)"
       The less customer information you hold, the more your chances are of becoming [GDPR](https://gdpr-info.eu/art-5-gdpr/) compliant.
       However, this does not mean that you let go of relevant data. It is important is to always ask: Do you need it?
   If you ever decide you need them you can always request them later

If on the other hand you don’t agree with what I just wrote or for the particular project you are currently working on
my configuration doesn’t work for you, removing django-improved-user should be an easy change.

First update the ``User`` models to look exactly like in the code below.

.. code-block:: python
   :caption: users/models.py

   from django.contrib.auth.models import AbstractUser

   class User(AbstractUser):
       pass

Then delete the ``forms.py``, ``admin.py`` and ``migrations/0001_initial.py`` files in the ``users`` app.
With that you should be good to go, if you want something a little more complete to start with you can grab some
code from the `cookiecutter-django users app <https://github.com/cookiecutter/cookiecutter-django/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/%7B%7Bcookiecutter.project_slug%7D%7D/users>`__.

HTMX and template partials
^^^^^^^^^^^^^^^^^^^^^^^^^^



DjangoFastDev
^^^^^^^^^^^^^

Occasionally you may see a ``FastDevVariableDoesNotExist`` error, this exception is thrown during template rendering
by `django-fastdev <https://github.com/boxed/django-fastdev>`__ when you try to access a variable that is not defined in the context
context of the view associated with that template. This is intended to help you avoid typos and small errors that will
have you scratching your head for hours, read the project `readme <https://github.com/boxed/django-fastdev#django-fastdev>`_ if you want more reasons
to why it make sense to use it. But since this can be annoying for some people, you can disable it by removing ``django-fastdev``
entirely or by commenting out the *django-fastdev* application in the ``settings.py`` file.

.. code:: python

   THIRD_PARTY_APPS = [
       ...
       # 'django_fastdev',
   ]

Dj Notebook
^^^^^^^^^^^

This is a recent addition to the project, It is basically using your django shell in a jupyter notebook. There is a ``playground.ipynb`` at the root of the generated
project, it configured with dj-notebook, I personnally find myself using it to keep some query in text so that I don't have to retype them everyone or search
through my command line history. You need to alwas run the first setting before anything to setup django. Also keep in mind that is does not automatically pickup
files changes so you'll have to restart the kernel to see changes.
If you a primer on jupyter notebook, you can find one `here <https://www.dataquest.io/blog/jupyter-notebook-tutorial/>`_.


Hatch for dependencies management
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Installed at the same time as ``pip-tools``, `Hatch <https://hatch.pypa.io/latest/>`__ is the build system specified in the ``pyproject.toml`` file. Since you are probably
not going to package and publish your django project you don’t really need it, but ``pip-tools`` does need a build system defined
to work.

    "Hatch is a modern, extensible Python project manager."

    -- Official hatch documentation


Hatch does everything you need to manage a python project, dependencies, virtual environments, packaging, publishing, scripts, etc and it also uses
the ``pyproject.toml`` file. The one available after the ``remove-poetry`` command is a good base to start using hatch.

Just run

.. code:: shell

   hatch env create

Read the `hatch documentation <https://hatch.pypa.io/latest/>`__ for more infos.

.. admonition:: Alias Hatch run
   :class: tip

   You could alias ``hatch run`` to ``hr`` to making typing hatch commands a bit faster.


The ``pyproject.toml`` file
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``pyproject.toml`` file is a python standard introduced to unify and simplify python project packaging and configurations.
The pip documentation gives much more details on this than I can cover here, so I will just link to it `here <https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/>`__.
A lot of tools (including hatch) in the python ecosystem support it and it seems this is what we are going to be using in the future so that's why I choose it.


Tailwind CSS
^^^^^^^^^^^^


Alternative starters
--------------------

* https://github.com/cookiecutter/cookiecutter-django
* https://github.com/oliverandrich/django-hatch-startproject
* https://github.com/oliverandrich/django-poetry-startproject
* https://github.com/jefftriplett/django-startproject
* https://github.com/wsvincent/djangox
* https://github.com/wemake-services/wemake-django-template
