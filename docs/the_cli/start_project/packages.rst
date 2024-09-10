:description: The packages and tools that comes included with a project generated with falco.

Packages and Tools
==================

This section provides an overview of the primary packages and tools, along with some of the design choices incorporated
into a project generated with **Falco**.

Overview
--------

System Requirements

- `hatch <https://hatch.pypa.io/latest/>`_: Used for managing the project's virtual environment and dependencies, more details can be found in the `dependency management guide </guides/dependency_management.html>`_.
- `just <https://just.system>`_: A script runner that simplifies the execution of common tasks, such as setting up the project, running the server, and running tests, run ``just`` to see all available commands.

Base Dependencies

- `environs <https://github.com/sloria/environs>`_: Used for configuring settings via environment variables.
- `django-allauth <https://github.com/pennersr/django-allauth>`_: Handles login and signup processes.
- `django-template-partials <https://github.com/carltongibson/django-template-partials>`_: Used for defining reusable fragments of HTML.
- `django-htmx <https://github.com/adamchainz/django-htmx>`_: Used for making AJAX requests and updating the DOM.
- `django-lifecycle <https://github.com/rsinger86/django-lifecycle>`_: Provides an alternative to signals for hooking into your model's lifecycle.
- `django-heath-check <https://github.com/revsys/django-health-check>`_: Provides a ``/health`` endpoint for application, database, storage, and other health checks.
- `django-extensions <https://django-extensions.readthedocs.io/en/latest/>`_: Adds some useful management commands to Django, such as ``shell_plus`` and ``show_urls``.
- `django-anymail <https://github.com/anymail/django-anymail>`_: `Amazon SES <https://aws.amazon.com/ses/?nc1=h_ls>`_ is used for production email, facilitated by Anymail.
- `django-unique-user-email <https://github.com/carltongibson/django-unique-user-email>`_: Adds a unique constraint to the email field of the Django ``User`` model.
- `django-q2 <https://github.com/django-q2/django-q2>`_: Used for background task queue processing and scheduling.
- `django-q-registry <https://github.com/westerveltco/django-q-registry>`_: Used for easily registering scheduled jobs.
- `django-storages <https://django-storages.readthedocs.io/en/latest/>`_: Used for storing media files on AWS S3.
- `django-compressor <https://github.com/django-compressor/django-compressor>`_: Compresses CSS and JavaScript files.
- `refreshcss <https://github.com/adamghill/refreshcss>`_: Removes unused classes, ids, and element selectors from CSS, configured as a ``django-compressor`` filter.
- `diskcache <https://github.com/grantjenks/python-diskcache>`_: A simple and fast cache solution based on ``sqlite3``, just add a ``LOCATION`` environnment folder for the cache location and you are good to go.
- `Docker <https://www.docker.com/>`_ and `s6-overlay <https://github.com/just-containers/s6-overlay>`_: Docker is configured for production, with s6-overlay enabling running both the web server process (via ``gunicorn``) and the background worker process (via ``django-q2``) within a single container.
- `Sentry <https://sentry.io/welcome/>`_: Utilized for performance and error monitoring.
- `Whitenoise <https://whitenoise.evans.io/en/latest/>`_: Used to serve static files.
- `heroicons <https://heroicons.com/>`_: Easy access to `heroicons <https://heroicons.com/>`_ in your Django templates.

Development-Only packages

- `django-debug-toolbar <https://django-debug-toolbar.readthedocs.io/en/latest/>`_: Of course, a must.
- `django-browser-reload <https://github.com/adamchainz/django-browser-reload>`_: Automatically reloads your browser on code changes in development.
- `django-watchfiles <https://github.com/adamchainz/django-watchfiles>`_: Faster and more efficient development server reloading.
- `django-fastdev <https://github.com/boxed/django-fastdev>`_: Helps catch small mistakes early in your project.
- `dj-notebook <https://github.com/pydanny/dj-notebook>`_: Allows you to use your shell_plus in a Jupyter notebook.
- `hatch-pip-compile <https://github.com/juftin/hatch-pip-compile>`_: ``hatch`` plugin to compile requirements files.
- `git-cliff <https://git-cliff.org/>`_: Generates a changelog based on your commit messages.
- `bump-my-version <https://github.com/callowayproject/bump-my-version>`_: Bumps the version of your project following the `semver <https://semver.org/>`_ format.
- `pytest <https://docs.pytest.org/en/7.0.x/>`_: Used for running tests
- `pytest-django <https://pytest-django.readthedocs.io/en/latest/>`_: Pytest plugin for Django.
- `pytest-sugar <https://github.com/Teemu/pytest-sugar>`_: Better looking pytest output.
- `pytest-xdist <https://github.com/pytest-dev/pytest-xdist>`_: Run tests in parallel.
- `Werkzeug <https://werkzeug.palletsprojects.com/en/2.1.x/>`_: Enable the Werkzeug debugger when running `manage.py runserver_plus`.
- `pre-commit <https://github.com/pre-commit/pre-commit>`_: Integrated by default to identify simple issues before pushing code to remote.

If you are using the default template, the following additional packages are included:

- `django-tailwind-cli <https://github.com/oliverandrich/django-tailwind-cli>`_: Integration with tailwind css using the `Tailwind CSS CLI <https://tailwindcss.com/blog/standalone-cli>`_, eliminating the need for Node.js.
- `crispy-tailwind <https://github.com/django-crispy-forms/crispy-tailwind>`_: Tailwind CSS Template pack for ``django-crispy-forms``.

If you are using the Bootstrap template, the following additional packages are included:

- `django-bootstrap5 <https://github.com/zostera/django-bootstrap5>`_: Integration with bootstrap 5 and provide some useful templates tags like ``bootstrap_messages`` to automatically render Django messages as bootstrap alerts.
- `crispy-bootstrap5 <https://github.com/django-crispy-forms/crispy-bootstrap5>`_: Bootstrap 5 Template pack for ``django-crispy-forms``.


Settings
--------

There is a single ``settings.py`` file located in your project directory. 

.. code-block:: text

   myjourney
   ├── myjourney
   │  ├── settings.py
   │  ...

As suggested in the `Twelve-Factor App <https://12factor.net/config>`_ methodology, the settings values are pulled from environment variables 
using `django-environ <https://github.com/sloria/environs>`_. Most settings are configured with default values or are made optional so that the project can be easily set up in development, production, or even a staging environment. 
The settings are organized following recommendations from `Boost Your Django DX <https://adamchainz.gumroad.com/l/byddx>`_.

There is no specific environment variable to distinguish between development and production environments. You can add that if you want, but I keep it simple:

- ``DEBUG=True`` means development
- ``DEBUG=False`` means production

You won't even be able to set ``DEBUG=True`` in production since the development requirements will be missing. They are not included in the provided methods of building the project for production.


Login via email instead of username
-----------------------------------

The ``email`` field is configured as the login field using `django-allauth <https://github.com/pennersr/django-allauth>`_. The ``username`` field is still present
but is not required for login. Allauth automatically fills it with the part of the email before the ``@`` symbol.
More often then not when I create a new django project I need to use something other than the ``username`` field provided by django as the unique identifier of the user,
and the ``username`` field just becomes an annoyance to deal with. It is also more common nowadays for modern web and mobile applications to rely on a unique identifier
such as an email address or phone number instead of a username.

.. important::

    There is a small fix applied for allauth related to django-fastdev in the ``core/apps.py`` file. Make sure to read it in case you ever need to change it.

.. admonition:: Custom user model
    :class: note dropdown

     I also removed the ``first_name`` and ``last_name`` fields that are available by default on the Django ``User`` model. I don't always need them, and when I do, I generally have a separate ``Profile``
     model to store users' personal informations, keeping the ``User`` model focused on authentication and authorization.
     My reasoning for this is to avoid asking for unnecessary data (following the principle of `YAGNI <https://en.wikipedia.org/wiki/You_aren%27t_gonna_need_it>`_). A positive consequence of this approach
     is that having less data on your users/customers increases the chances of being `GDPR compliant <https://gdpr.eu/compliance/>`_. You can always add these fields later if needed.

     -- me, not so long ago

    Previously, this section of the docs contained the message above. Now, I take a simpler approach: Falco doesn't ship with a custom user model anymore, and I don't recommend having one for most people. There are
    now even better resources I can link to that explain why this is better than I could ever do:

    - https://noumenal.es/posts/django-unique-user-email/928/
    - https://buttondown.com/carlton/archive/evolving-djangos-authuser/

    If you need to save user data, a profile model is a better approach, and better field names are ``full_name`` and ``short_name``. For the reasoning behind this, check out
    https://django-improved-user.readthedocs.io/en/latest/rationale.html

HTMX and template partials
--------------------------

The project comes set up with django-template-partials_ and htmx_ for the times when you need to add some
interactivity to your web app. The `interactive user interfaces guide </guides/interactive_user_interfaces.html>`_ goes into more detail on this, but for a brief overview:

* django-template-partials_ is used to define reusable fragments of HTML
* htmx_'s job is to make requests to the backend, get a piece of HTML fragment in response, and patch the `DOM <https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction>`_ using it. Basically, htmx allows you to write declarative code to make `AJAX <https://www.w3schools.com/xml/ajax_intro.asp>`_ (Asynchronous JavaScript And XML) requests.

.. admonition:: jetbrains extensions
    :class: tip dropdown

    If you are using a jetbrains IDE, there is an extension that add support for htmx, you can find it `here <https://plugins.jetbrains.com/plugin/20588-htmx-support>`_.
    If you use `alpinejs <https://alpinejs.dev/>`_ there is also for it via `this extension <https://plugins.jetbrains.com/plugin/15251-alpine-js-support>`_.

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

Background tasks and scheduling
-------------------------------

`django-q2 <https://github.com/django-q2/django-q2>`_ is my preferred background task queue system for Django. In most projects, I always utilize either the task queue processing,
scheduling, or sometimes both. Regarding scheduling, there is also `django-q-registry <https://github.com/westerveltco/django-q-registry>`_ included, which is a ``django-q2`` extension
that helps with easily registering scheduling jobs.

Here is an example of how using both looks:

.. tabs::

    .. tab:: tasks.py

        .. code-block:: python
            :caption: tasks.py

            from django.core.mail import send_mail
            from django_q.models import Schedule
            from django_q_registry import register_task

            @register_task(
                name="Send periodic test email",
                schedule_type=Schedule.MONTHLY,
            )
            def send_test_email():
                send_mail(
                    subject="Test email",
                    message="This is a test email.",
                    from_email="noreply@example.com",
                    recipient_list=["johndoe@example.com"],
                )


            def long_running_task(user_id):
                # a simple task meant to be run in background
                ...

    .. tab:: views.py

        .. code-block:: python
            :caption: views.py

            from django_q.tasks import async_task
            from .tasks import long_running_task

            def my_view(request):
                task_id = async_task(long_running_task, user_id=request.user.id)
                ...

It is a good idea to organize any task or scheduling job function in a ``tasks.py`` file in the relevant Django application.

.. hint::

    For more details on task queues and scheduling, check out `my guide on the topic </guides/task_queues_and_schedulers.html/>`_.


Model lifecycle
---------------

`django-lifecycle <https://github.com/rsinger86/django-lifecycle>`_ offers an alternative to `signals <https://docs.djangoproject.com/en/dev/topics/signals/>`_ for hooking into your model's lifecycle.
It provides a more readable and understandable way to write code that runs before or after a model instance is created or updated, based on certain conditions. This code is placed directly on
the concerned models, which aligns well with Django's `fat models` philosophy.

Here is an example of using ``django-lifecycle`` straight from their README:

.. code-block:: python

   from django_lifecycle import LifecycleModel, hook, BEFORE_UPDATE, AFTER_UPDATE
   from django_lifecycle.conditions import WhenFieldValueIs, WhenFieldValueWas, WhenFieldHasChanged


   class Article(LifecycleModel):
      contents = models.TextField()
      updated_at = models.DateTimeField(null=True)
      status = models.ChoiceField(choices=['draft', 'published'])
      editor = models.ForeignKey(AuthUser)

      @hook(BEFORE_UPDATE, WhenFieldHasChanged("contents", has_changed=True))
      def on_content_change(self):
         self.updated_at = timezone.now()

      @hook(AFTER_UPDATE,
        condition=(
            WhenFieldValueWas("status", value="draft")
            & WhenFieldValueIs("status", value="published")
        )
      )
      def on_publish(self):
         send_email(self.editor.email, "An article has published!")


DjangoFastDev
-------------

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
-----------

This package allows you to use your `shell_plus <https://django-extensions.readthedocs.io/en/latest/shell_plus.html>`_ in a Jupyter notebook.
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

   os.environ["DJANGO_SETTINGS_MODULE"] = "<your_project>.settings"
   django.setup()



Entry point and Binary
----------------------

There is a `__main__.py <https://docs.python.org/3/library/__main__.html#main-py-in-python-packages>`_ file inside your project directory, next to your ``settings.py`` file.
This is the main entry point of your app. This is what the binary app built with `pyapp <https://github.com/ofek/pyapp>`_ effectively uses. Commands run inside the Docker container also use this file.
This file can essentially replace your ``manage.py`` file, but the ``manage.py`` is retained since this is what most django devs are familiar with.

.. admonition:: More on this binary file thing
   :class: note dropdown

   The binary file that ``pyapp`` builds is a script that bootstraps itself the first time it is run, meaning it will create its own isolated virtual environment with **its own Python interpreter**.
   It installs the project (your falco project is setup as a python package) and its dependencies. When the binary is built, either via the provided GitHub Action or the ``just`` recipe / command,
   you also get a wheel file (the standard format for Python packages). If you publish that wheel file on PyPI, you can use the binary's ``self update`` command to update itself.

Let's assume you generated a project with the name ``myjourney``:

.. code-block:: shell
   :caption: Example of how to invoke the script

   just run python myjourney/__main__.py
   just run python -m myjourney
   just run myjourney

All the commands above do exactly the same thing.

.. code-block:: shell
   :caption: Usage Example

   just run myjourney # Runs the production server (gunicorn)
   just run myjourney qcluster # Runs the django-q2 worker for background tasks
   just run myjourney setup # Runs the setup function in the __main__.py file, runs migrations, createsuperuser, etc.
   just run myjourney manage runserver # Runs the django dev server
   just run myjourney manage dbshell # Opens the dbshell

The binary is automatically built on every new push via the GitHub Action in the ``.github/workflows/cd.yml`` file. You can also build it locally by running the following commands:

.. code-block:: shell
   :caption: Building the binary

   just build-bin # Builds for the current platform and architecture (e.g., if you are on an Intel macOS, it will build for macOS x86_64)
   just build-linux-bin # Always builds for Linux x86_64

For more details on deploying the binary to a VPS, check out the `deployment guide </the_cli/start_project/deploy.html>`_.


Project versioning
------------------

It is always a good idea to keep a versioning system in place for your project. The project includes the following tools to make the process as simple and low maintenance as possible:

- `git-cliff <https://git-cliff.org/>`_: Generate changelog for your project based on your commit messages, provided they follow the `conventional commits <https://www.conventionalcommits.org/en/v1.0.0/>`_ format.
- `bump-my-version <https://github.com/callowayproject/bump-my-version>`_: As the name suggests, it bumps the version of your project following the `semver <https://semver.org/>`_ format and creates a new git tag.

Both of these tools' configurations are stored in the ``pyproject.toml`` file under the ``[tool.git-cliff]`` and ``[tool.bumpversion]`` sections, respectively.

Additionally, there is a ``.github/workflows/cd.yml`` file that defines GitHub Actions that run every time you push new tags to your repository. This will push your changes to the server,
build wheels and binary for the project, and create a new GitHub release with the latest content from the ``CHANGELOG.md`` file. More details on this can be found in the `deployment guide </the_cli/start_project/deploy.html>`_.

Here is an example of the workflow:

Let's assume your project is at version ``0.0.1``, the initial version for new projects defined in the ``pyproject.toml`` file.
You make a few commits following the `conventional commits <https://www.conventionalcommits.org/en/v1.0.0/>`_ format, for example:

.. code-block:: shell
    :caption: Just an example to show commit messages

    git commit -m "feat: add new feature"
    git commit -m "fix: fix a bug"
    git commit -m "feat: add another feature"

Then you are ready for the first minor release. Following the `semver <https://semver.org/>`_ convention, that is equivalent to moving from ``0.0.1`` to ``0.1.0``.
You run the following command:

.. code-block:: shell

    just bumpver minor

This will bump the version of your project to ``0.1.0``, update the ``CHANGELOG.md`` file with the latest commits, and create a new git tag with the name ``v0.1.0`` and
push the tag to the remote repository, which will trigger the GitHub Action to create a new release with the content of the ``CHANGELOG.md`` file, build the binary and
deploy the project to the server.


Continuous Integration
----------------------

The file at ``.github/workflows/ci.yml`` is responsible for `Continuous Integration <https://en.wikipedia.org/wiki/Continuous_integration>`_.
Every time you push new changes to the main branch or create pull requests, an action is triggered to run tests, deployment checks, and type checks. This ensures nothing has broken
from the previous commit (assuming you write tests).
The content of the file is quite simple to read and understand. The main thing to note is that the workflow file only contains Just recipe commands. The actual commands are all defined in the justfile, so that you can easily run them locally if needed
or migrate to another CI/CD provider if you want to.

.. code-block:: shell
    :caption: Example of commands related to CI

    just types # run type checks with mypy
    just test # run tests with pytest
    just deploy-checks # run django deployment checks

Documentation
-------------

The documentation uses a basic `sphinx <https://www.sphinx-doc.org/en/master/>`_ setup with the `furo <https://github.com/pradyunsg/furo>`_ theme.
There is a basic structure in place that encourages you to structure your documentation based on your `django applications <https://docs.djangoproject.com/en/dev/ref/applications/>`_.
By default, you are meant to write using `reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_, but the `myst-parser <https://myst-parser.readthedocs.io/en/latest/>`_ is configured so
that you can use `markdown <https://www.markdownguide.org/>`_. Even if you are not planning to have very detailed and highly structured documentation (for some ideas on that, check out the `documentation writing guide </guides/writing_documentation.html>`_),
it can be a good place to keep notes on your project architecture, setup, external services, etc. It doesn't have to be optimal to be useful.

 "The Palest Ink Is Better Than the Best Memory."

 --- Chinese proverb

.. code-block:: shell
    :caption: Example of commands related to documentation

    just docs-build # build the documentation into a static site
    just docs-serve # serve the documentation locally on port 8001
    just docs-upgrade # upgrade the documentation dependencies


.. _hatch: https://hatch.pypa.io/latest/
.. _django-template-partials: https://github.com/carltongibson/django-template-partials
.. _htmx: https://htmx.org/
.. _django-htmx: https://github.com/adamchainz/django-htmx
.. _dj-notebook: https://github.com/pydanny/dj-notebook
.. _tailwindcss: https://tailwindcss.com
.. _django-tailwind-cli: https://github.com/oliverandrich/django-tailwind-cli

