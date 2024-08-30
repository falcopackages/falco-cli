:image: https://raw.githubusercontent.com/Tobi-De/falco/main/assets/og-image.jpg
:description: The packages and tools that comes included with a project generated with falco.

Packages and Tools
==================

This section provides an overview of the primary packages and tools, along with some of the design choices incorporated
into a project generated with **Falco**.


- `Hatch <https://hatch.pypa.io/latest/>`_: Used for managing the project's virtual environment and dependencies, more details can be found in the `dependency management guide </guides/dependency_management.html>`_.
- `Just <https://just.system>`_: A script runner that simplifies the execution of common tasks, such as setting up the project, running the server, and running tests, run ``just`` to see all available commands.
- `environs <https://github.com/sloria/environs>`_: Used for configuring settings via environment variables.
- `django-allauth <https://github.com/pennersr/django-allauth>`_: Handles login and signup processes.
- `django-debug-toolbar <https://django-debug-toolbar.readthedocs.io/en/latest/>`_: Of course, a must.
- `django-heath-check <https://github.com/revsys/django-health-check>`_: Provides a ``/health`` endpoint for application, database, storage, and other health checks.
- `django-browser-reload <https://github.com/adamchainz/django-browser-reload>`_: Automatically reloads your browser on code changes in development.
- `django-model-utils <https://django-model-utils.readthedocs.io/en/latest/>`_: Provides useful mixins for Django models, my favorite being the ``TimeStampedModel``.
- `django-extensions <https://django-extensions.readthedocs.io/en/latest/>`_: Adds some useful management commands to Django, such as ``shell_plus`` and ``show_urls``.
- `django-anymail <https://github.com/anymail/django-anymail>`_: `Amazon SES <https://aws.amazon.com/ses/?nc1=h_ls>`_ is used for production email, facilitated by Anymail.
- `django-storages <https://django-storages.readthedocs.io/en/latest/>`_: Used for storing media files on AWS S3.
- `django-compressor <https://django-compressor.readthedocs.io/en/latest/>`_: Compresses CSS and JavaScript files.
- `refreshcss <https://github.com/adamghill/refreshcss>`_: Removes unused classes, ids, and element selectors from CSS, configured as a ``django-compressor`` filter.
- `diskcache <https://github.com/grantjenks/python-diskcache>`_: A simple and fast cache solution based on ``sqlite3``, just add a ``LOCATION`` environnment folder for the cache location and you are good to go.
- `Docker <https://www.docker.com/>`_ and `s6-overlay <https://github.com/just-containers/s6-overlay>`_: Docker is configured for production, with s6-overlay enabling concurrent operation of ``django`` and ``django-q`` within a single container.
- `Sentry <https://sentry.io/welcome/>`_: Utilized for performance and error monitoring.
- `Whitenoise <https://whitenoise.evans.io/en/latest/>`_: Used to serve static files.
- `heroicons <https://heroicons.com/>`_: Easy access to `heroicons <https://heroicons.com/>`_ in your Django templates.
- `pre-commit <https://github.com/pre-commit/pre-commit>`_: Integrated by default to identify simple issues before pushing code to remote.

If you are using the default template, you will also find the following packages:

- `django-tailwind-cli <https://github.com/oliverandrich/django-tailwind-cli>`_: Integration with tailwind css using the `Tailwind CSS CLI <https://tailwindcss.com/blog/standalone-cli>`_, eliminating the need for Node.js.
- `crispy-tailwind <https://github.com/django-crispy-forms/crispy-tailwind>`_: Tailwind CSS Template pack for ``django-crispy-forms``.

If you are using the Bootstrap template, you will find:

- `django-bootstrap5 <https://github.com/zostera/django-bootstrap5>`_: Integration with bootstrap 5 and provide some useful templates tags like ``bootstrap_messages`` to automatically render Django messages as bootstrap alerts.
- `crispy-bootstrap5 <https://github.com/django-crispy-forms/crispy-bootstrap5>`_: Bootstrap 5 Template pack for ``django-crispy-forms``.


Login via email instead of username
------------------------------------

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

Django-q2
---------

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


Lifecycle not signals
---------------------

`django-lifecycle <https://github.com/rsinger86/django-lifecycle>`_  offers an alternative way of hooking into your models lifecycle  instead of writing django `signals <https://docs.djangoproject.com/en/dev/topics/signals/>`_ that I find more easily to read, understand,
follow, reason about and that is for aligned with the ``fat models`` models approach of django.

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

   os.environ["DJANGO_SETTINGS_MODULE"] = "<your_project>.settings"
   django.setup()



Project versioning
------------------

It is always a good ideas to keep a versionning system in place for your project. The project comes with following tools to make the process as smooth as possible.

- `git-cliff <https://git-cliff.org/>`_: Generate changelog for your project based on your commites messages, provided they follow the `conventional commits <https://www.conventionalcommits.org/en/v1.0.0/>`_ format.
- `bump-my-version <https://github.com/callowayproject/bump-my-version>`_: Lke the name suggest it bump the version of your project following the `semver <https://semver.org/>`_ format and additionnals create new git tags.

Both of these tools configurations are stored in the ``pyproject.toml`` file.

Then there is the ``.github/workflows/cd.yml`` file that defined github actions that are run everything your push new tags to your repository. These tasks include



https://www.conventionalcommits.org/en/v1.0.0/
https://semver.org/

Continuous Integration
----------------------

This directory is a GitHub-specific folder, meant for configurations related to GitHub like bots, GitHub Actions workflows, etc.
At the root of the folder, you'll see a ``dependabot.yml`` file. It is a config file for `Dependabot <https://github.com/dependabot>`_ that is configured to
check weekly for dependency upgrades in your requirements files (more on that in the virtualenv management section). 
There is a workflow directory with a ``ci.yml`` file (CI stands for `Continuous Integration <https://en.wikipedia.org/wiki/Continuous_integration>`_). 
This file is meant to run tests, deployment checks, and type checks every time you push a new commit to GitHub to make sure nothing has broken 
from the previous commit (assuming you do write tests).


Fo the continuous deployment (CD) checkout the `deployment </the_cli/start_project/deploy.html>`_ guide.

Documentation
-------------

The documentation uses a basic `sphinx <https://www.sphinx-doc.org/en/master/>`_ setup with the `furo <https://github.com/pradyunsg/furo>`_ theme. 
There is a basic structure in place that encourages you to structure your documentation based on your `django applications <https://docs.djangoproject.com/en/dev/ref/applications/>`_. 
By default, you are meant to write using `reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_, but the `myst-parser <https://myst-parser.readthedocs.io/en/latest/>`_ is configured so 
that you can use `markdown <https://www.markdownguide.org/>`_. Even if you are not planning to have very detailed and highly structured documentation (for some ideas on that, check out the `documentation writing guide </guides/writing_documentation.html>`_), 
it can be a good place to keep notes on your project architecture, setup, external services, etc. It doesn't have to be optimal to be useful.

 "The Palest Ink Is Better Than the Best Memory."

 --- Chinese proverb



.. _hatch: https://hatch.pypa.io/latest/
.. _django-template-partials: https://github.com/carltongibson/django-template-partials
.. _htmx: https://htmx.org/
.. _django-htmx: https://github.com/adamchainz/django-htmx
.. _dj-notebook: https://github.com/pydanny/dj-notebook
.. _tailwindcss: https://tailwindcss.com
.. _django-tailwind-cli: https://github.com/oliverandrich/django-tailwind-cli

