:image: https://raw.githubusercontent.com/Tobi-De/falco/main/assets/og-image.jpg
:description: start a new django project ready for your next saas idea.

Start project
=============

.. cappa:: falco.commands.StartProject

Initialize a new django project the falco way. This project-starter makes several assumptions; we'll go through the most important choices I made below.
I'll list some alternatives below in case you don't agree with my choices. But even if you choose to use an alternative, most commands
can still be useful to you, and the `guides </guides/index.html>`_ are not particularly tied to the generated project. So, even with another project-starter, **Falco**
can still bring you value.

.. code-block:: bash
   :caption: Example

   $ falco start-project myproject



.. note::

   The **authors** key of the ``[tool.project]`` section in the ``pyproject.toml`` is set using your git global user
   configuration. If you haven't set it yet, `see this page <https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup#_your_identity>`_.


Features
--------

- Python 3.11+
- Django 5+
- Htmx_ integration via django-htmx_
- Frontend CSS: tailwindcss_ via django-tailwind-cli_
- Template fragment with django-template-partials_
- Background tasks with `django-q2 <https://github.com/django-q2/django-q2>`_
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
- Dependency management using hatch_
- Playground file for local testing with dj-notebook_.

.. tip::

   If you are using a jetbrains IDE, there is an extension that add support for htmx, you can find it `here <https://plugins.jetbrains.com/plugin/20588-htmx-support>`_.
   If you use `alpinejs <https://alpinejs.dev/>`_ there is also for it via `this extension <https://plugins.jetbrains.com/plugin/15251-alpine-js-support>`_.


Project Structure
-----------------

Now w'll go through more details about the structure, layouts and packages used for the project template and therefore available
in your generated project.


.. figure:: ../images/project-tree.svg

With this layout, your local apps reside in a subdirectory with the same name as your project. Every time you create a new app,
you should move it to that subdirectory and rename it (e.g., from ``myapp`` to ``myproject.myapp``) in the ``apps.py`` file.

.. admonition:: hatch run start-app
   :class: dropdown note

   There is a default script included with the project that automates this process. You can trigger it by running
   ``hatch run start-app products``, and it will create the app using the Django ``startapp`` command, move it to your apps directory, and rename it.
   However, you won't be able to pass additional commands to the original `django startapp command <https://docs.djangoproject.com/en/dev/ref/django-admin/#startapp>`_ (i.e., ``--name`` to specify file names), and the app
   won't be automatically registered in your ``INSTALLED_APPS``.

All your project configurations, settings, URLs, WSGI app file, etc., reside in the ``config`` folder.

The ``deploy`` folder contains some files that are needed for deployment, mainly docker related. If Docker isn't part of your deployment plan, this directory can be safely removed.
However, you might want to retain the ``gunicorn.conf.py`` file inside that directory, which is a basic Gunicorn configuration file that could be useful regardless of your chosen deployment strategy.

Login via email instead of username
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

I completely removed the ``username`` field from the ``User`` model and replaced it with the ``email`` field as the user unique identifier.
The ``email`` field is what I configured as the login field using `django-allauth <https://github.com/pennersr/django-allauth>`_.
More often then not when I create a new django project I need to use something other than the ``username`` field provided by django as the unique identifier of the user,
and the ``username`` field just becomes an annoyance to deal with. It is also more common nowadays for modern web and mobile applications to rely on a unique identifier
such as an email address or phone number instead of a username.

I also removed the ``first_name`` and ``last_name`` fields that are available by default on the Django ``User`` model. I don't always need them, and when I do, I generally have a separate ``Profile``
model to store users' personal informations, keeping the ``User`` model focused on authentication and authorization.
My reasoning for this is to avoid asking for unnecessary data (following the principle of `YAGNI <https://en.wikipedia.org/wiki/You_aren%27t_gonna_need_it>`_). A positive consequence of this approach
is that having less data on your users/customers increases the chances of being `GDPR compliant <https://gdpr.eu/compliance/>`_. You can always add these fields later if needed.

.. admonition:: django-unique-user-email
   :class: note dropdown

   There is a package called `django-unique-user-email <https://github.com/carltongibson/django-unique-user-email>`_ by `Carlton Gibson <https://twitter.com/carlton_gibson>`_, a core Django contributor, that
   allows you to use email as the primary identifier for authentication without modifying the default ``User`` model. This package eliminates the need to create a custom ``User`` model. Although I considered
   including this package by default (less code is better), it might be too radical to use at the moment.

However, if my arguments are not convincing enough or for the particular project you are working you need to have the
username field on your ``User`` model for login purposes, the required changes are quite simple and can be summarized as follows:

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

The project comes set up with django-template-partials_ and htmx_ for the times when you need to add some
interactivity to your web app. The `interactive user interfaces guide </guides/interactive_user_interfaces.html>`_ goes into more detail on this, but for a brief overview:

* django-template-partials_ is used to define reusable fragments of HTML
* htmx_'s job is to make requests to the backend, get a piece of HTML fragment in response, and patch the `DOM <https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction>`_ using it. Basically, htmx allows you to write declarative code to make `AJAX <https://www.w3schools.com/xml/ajax_intro.asp>`_ (Asynchronous JavaScript And XML) requests.

Let's look at a quick example:

.. code-block:: django
   :linenos:
   :caption: elements.html
   :emphasize-lines: 4, 6, 11-13


   {% block main %}
   <ul id="element-list">
      {% for el in elements %}
         {% partialdef element-partial inline=True %}
            <li>{{ el }}</li>
         {% endpartialdef %}
      {% endfor %}
   </ul>

   <form
   hx-post="{% url 'add_element' %}"
   hx-target="#element-list"
   hx-swap="beforeend"
   >
      <!-- Let's assume some form fields are defined here -->
      <button type="submit">Submit</button>
   </form>

   {% endblock main %}

The htmx attributes (prefixed with ``hx-``) defined above basically say:

 when the form is submitted, make an asynchronous JavaScript request to the URL ``{% url 'add_element' %}`` and add the content of the response before the end (before the last child) element of the element with the ID ``element-list`` .

The complementary Django code on the backend would look something like this:

.. code-block:: python
   :linenos:
   :caption: views.py
   :emphasize-lines: 6

   def add_element(request):
      new_element = add_new_element(request.POST)
      if request.htmx:
         return render(request, "myapp/elements.html#element-partial", {"el": new_element})
      else:
         redirect("elements_list")

The highlighted line showcases a syntax feature provided by django-template-partials_. It enables you to selectively
choose the specific HTML fragment from the ``elements.html`` file that is enclosed within the ``partialdef`` tag with the name ``element-partial``.

The ``htmx`` attribute on the ``request`` element is provided by django-htmx_, which is already configured in the project.

This example illustrates how you can create a button that adds a new element to a list of elements on a page without reloading the entire page.
Although this might not seem particularly exciting, the `interactive user interfaces guide </guides/interactive_user_interfaces.html>`_ provides more
practical examples that demonstrate the extensive possibilities offered by this approach.


DjangoFastDev
^^^^^^^^^^^^^

The DjangoFastDev package helps catch small mistakes early in your project. When installed you may
occasionally encounter a ``FastDevVariableDoesNotExist`` error, this exception is thrown during template rendering
by `django-fastdev <https://github.com/boxed/django-fastdev>`_ when you try to access a variable that is not defined in the context
of the view associated with that template. This is intended to help you avoid typos and small errors that will
have you scratching your head for hours, read the project `readme <https://github.com/boxed/django-fastdev#django-fastdev>`_ to see
all the features it provides.
If you find the package's errors to be too frequent or annoying, you can disable it by removing the ``django-fastdev`` application
entirely or by commenting it out in the ``settings.py`` file.


.. code:: python

   THIRD_PARTY_APPS = [
       ...
       # 'django_fastdev',
   ]

Dj Notebook
^^^^^^^^^^^

This is a recent addition to the project. It allows you to use your `shell_plus <https://django-extensions.readthedocs.io/en/latest/shell_plus.html>`_ in a Jupyter notebook.
In the root of the generated project, you will find a file named ``playground.ipynb`` which is configured with dj-notebook_.
As the name suggests, I use this as a playground to play with the Django ORM. Having it saved in a file is particularly useful for storing frequently used queries in text format,
eliminating the need to retype them or search through command line history. Before running any additional cells you add, make sure to run the first cell in the notebook to set up Django. It's
important to note that dj-notebook_ does not automatically detect file changes, so you will need to restart the kernel after making any code modifications.
If you need a refresher on Jupyter notebooks, you can refer to this `primer <https://www.dataquest.io/blog/jupyter-notebook-tutorial/>`_.

**Marimo**

There is a new alternative to Jupyter notebooks, namely, `marimo <https://marimo.io/>`_. The main features that I appreciate are:

- Notebooks are straightforward Python scripts.
- It has a beautiful UI.
- It provides a really nice tutorial: ``pip install marimo && marimo tutorial intro``.

Its main advertised feature is having reactive notebooks, but for my use case in my Django project, I don't really care about that.

If you want to test ``marimo`` with your Django project, it's quite simple. Install it in your project environment and run:

.. code-block:: shell

   marimo edit notebook.py

Or using hatch:

.. code-block:: shell

   hatch run marimo edit notebook.py

As with ``dj-notebook``, for your Django code to work, you need some kind of activation mechanism. With ``dj-notebook``, the first cell needs to run the code ``from dj_notebook import activate; plus = activate()``. With ``marimo``, the cell below should do the trick.



.. code-block:: python

   import django
   import os

   os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
   django.setup()


Virtualenv and Dependencies Management
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is mainly handled using ``hatch``, ``hatch-pip-compile``, and the ``pyproject.toml`` file.

The pyproject.toml File
***********************

The ``pyproject.toml`` file is a Python standard introduced to unify and simplify Python project packaging and configurations. It was introduced by `PEP 518 <https://www.python.org/dev/peps/pep-0518/>`_ and `PEP 621 <https://www.python.org/dev/peps/pep-0621/>`_.
For more details, check out the `complete specifications <https://packaging.python.org/en/latest/specifications/pyproject-toml/#pyproject-toml-spec>`_.
Many tools in the Python ecosystem, including hatch, support it, and it seems that this is what the Python ecosystem has settled on for the future.

Hatch
*****

The project is set up to use hatch_ for virtual environment management and dependencies management.

   "Hatch is a modern, extensible Python project manager."

   -- Official hatch documentation

Read the hatch documentation on `environment <https://hatch.pypa.io/latest/environment/>`_ for more information on how to manage virtual environments.
Hatch can do a lot, including `managing Python installations <https://hatch.pypa.io/latest/cli/reference/#hatch-python>`_, but for the context of the project, these are the things you need to know.

Activate the virtual environment
++++++++++++++++++++++++++++++++

To activate the default virtual environment, run:

.. code-block:: bash

   $ hatch shell

You don't need to activate your shell to run commands. When using ``hatch run``, dependencies will be automatically synced (installed or removed if necessary) and the command will be
executed in the appropriate virtual environment.

For instance, to run the Django development server, you can use the following command:

.. code-block:: bash

   $ hatch run python manage.py runserver

This will run your project in the default virtual environment.

Add / remove a new dependency
+++++++++++++++++++++++++++++

The default virtual environment includes all the dependencies specified in the ``[project.dependencies]`` section of the ``pyproject.toml`` file.
To add a new dependency to your project, simply edit the ``pyproject.toml`` file and add it to the ``[project.dependencies]`` section.
The next time you run a command using hatch, such as ``hatch run python manage.py runserver``, hatch will automatically install the new dependency.
The process is the same for removing a dependency.

Scripts
+++++++

The ``pyproject.toml`` file in the project defines some convenient scripts for common commands in a Django project. The section looks something like this:

.. code-block:: toml

   [tool.hatch.envs.default.scripts]
   runserver = ["migrate", "python manage.py tailwind runserver {args}"]
   migrate = "python manage.py migrate {args}"
   makemigrations = "python manage.py makemigrations {args}"
   ...

To start the Django development server for example, you can use the command ``hatch run runserver``.

.. admonition:: Alias Hatch run
   :class: tip

   To make typing hatch commands faster, you can create an alias for ``hatch run``. For example, you can alias it as ``hr``. So,
   Instead of typing ``hatch run runserver``, you can simply use the alias ``hr runserver``. However, please note that if your system takes time to resolve the alias,
   it may impact your overall experience.

For development, I think this workflow should work quite well. Now, what happens when you need to deploy your app? You could install hatch on
the deploy target machine, but I prefer having a ``requirements.txt`` file that I can use to install dependencies on the deployment machine.
That's where ``hatch-pip-compile`` comes in.

.. admonition:: why hatch?
   :class: dropdown note

   Using hatch is a recent switch for me. Previously, I used `poetry <https://python-poetry.org/>`_ as my preferred tool. While poetry is still a great tool, I have chosen hatch for the following reasons:

   1. Backed by the **pypa** (Python Packaging Authority), hatch aligns with the efforts to solve packaging and tooling issues in the Python ecosystem. I believe that if the Python ecosystem ever manages to overcome these challenges, it will be because the pypa has reached a consensus, and I hope that hatch will be the chosen solution. We all hope to see a cargo-like tool for Python someday.

   2. Hatch now has the ability to install and manage Python versions, along with other existing features. This brings it closer to being the all-in-one tool that every Python developer needs.

   3. Hatch is PEP-friendly, making it compatible with other tools in the ecosystem. It adds minimal custom configuration to the ``pyproject.toml`` file and relies on existing standards for project information and dependencies.

   4. In terms of performance, hatch is faster compared to poetry. While poetry is generally not slow, there have been rare instances where it took 30 minutes to install requirements. I have experienced this a few times.


hatch-pip-compile
*****************

The `hatch-pip-compile <https://github.com/juftin/hatch-pip-compile>`_ plugin is used with hatch to automatically generate a
requirements file (lock file) using `pip-tools <https://github.com/jazzband/pip-tools>`_. This file contains the dependencies of your hatch virtual environment with pinned versions.
The default setup generates a ``requirements.txt`` file that can be used for installing dependencies during deployment, as shown in the provided Dockerfile. However, you can customize the plugin to save
locks for all your environments. Refer to the `hatch-pip-compile documentation <https://github.com/juftin/hatch-pip-compile>`_ for more details.

Here is the current configuration in the ``pyproject.toml`` file relevant to hatch-pip-compile:

.. code-block:: toml

   [tool.hatch.env]
   requires = [
   "hatch-pip-compile"
   ]

   [tool.hatch.envs.default]
   type = "pip-compile"
   pip-compile-constraint = "default"
   pip-compile-installer = "pip-sync"
   lock-filename = "requirements.txt"



Working without hatch
*********************

You don't have to use Hatch if you don't want to. Thanks to Hatch being very PEP-friendly, you can use the ``pyproject.toml`` file with recent versions of
pip to install the main dependencies of the project. You won't be able to use the scripts (for that, you can use `peothepoet <https://github.com/nat-n/poethepoet>`_) or any other Hatch features,
but you may not need them.

Let's assume you want to use the classic ``venv``. Here's what the workflow would look like:

1. Remove any Hatch-related configuration from the pyproject.toml file, including anything starting with ``[tool.hatch]``. This step is optional and up to your choice.
2. Create a virtual environment using ``python -m venv venv``.
3. Activate the virtual environment using ``source venv/bin/activate``.
4. Install the dependencies using ``pip install -e .``. This command will install your project and its dependencies using the ``pyproject.toml`` file.

To add or remove dependencies, the process is the same. You edit the ``[project.dependencies]`` section of the pyproject.toml file and run ``pip install -e .``. You can complement
this workflow with `pip-tools <https://github.com/jazzband/pip-tools>`_ to generate a requirements file.


..
.. CSS Framework
.. ^^^^^^^^^^^^^

.. The project starter is setup to use to tailwindcss_ via django-tailwind-cli_, there is also crispy-tailwind for tailwind süppport for crispy.
.. Currently taiwindcss is the less painfull way for me to write css. I stil use bootstrap5 everyday but mostly and it still the best way for a lot of people,
.. the change to bootstrap is quite simple.

Known issues
------------

Here is a collection of known issues and their solutions that you may encounter when using the project starter.

hatch-pip-compile
^^^^^^^^^^^^^^^^^

In my experience, the hatch-pip-compile plugin may not function properly if hatch is not installed using a `binary <https://hatch.pypa.io/latest/install/#standalone-binaries>`_.
Therefore, ensure that you have the latest version of hatch (at least 1.8.0) and that you have installed it using the binary distribution.

hatch and pre-commit
^^^^^^^^^^^^^^^^^^^^

If you encounter an error when trying to make a commit after installing the pre-commit hooks, the error message may look like this:

.. code-block:: bash

   $ An unexpected error has occurred: PermissionError: [Errno 13] Permission denied: '/usr/local/hatch/bin/hatch' Check the log at /Users/tobi/.cache/pre-commit/pre-commit.log

To resolve this issue, you can change the owner of the hatch binary using the following command:

.. code-block:: bash

   $ sudo chown $USER /usr/local/hatch/bin/hatch

If you are unsure of the location of your hatch binary, you can use the following command to change the owner:

.. code-block:: bash

   $ sudo chown $USER $(which hatch)


pre-commit python version
^^^^^^^^^^^^^^^^^^^^^^^^^

If you encounter the following error:

.. code-block:: shell

   RuntimeError: failed to find interpreter for Builtin discover of python_spec='python3.11'

You need to update the section below (located at the beginning of the ``.pre-commit-config.yaml`` file) to match the Python version in your virtual environment:

.. code-block:: yaml

   default_language_version:
      python: python3.11 # TODO: Change this to match your virtual environment's Python version


Alternative starters
--------------------

Here are some alternative project starters that you can consider if the falco starter is not to your liking:

- `cookiecutter-django <https://github.com/cookiecutter/cookiecutter-django>`_
- `django-hatch-startproject <https://github.com/oliverandrich/django-hatch-startproject>`_
- `django-poetry-startproject <https://github.com/oliverandrich/django-poetry-startproject>`_
- `django-startproject <https://github.com/jefftriplett/django-startproject>`_
- `djangox <https://github.com/wsvincent/djangox>`_
- `wemake-django-template <https://github.com/wemake-services/wemake-django-template>`_


.. _hatch: https://hatch.pypa.io/latest/
.. _django-template-partials: https://github.com/carltongibson/django-template-partials
.. _htmx: https://htmx.org/
.. _django-htmx: https://github.com/adamchainz/django-htmx
.. _dj-notebook: https://github.com/pydanny/dj-notebook
.. _tailwindcss: https://tailwindcss.com
.. _django-tailwind-cli: https://github.com/oliverandrich/django-tailwind-cli
