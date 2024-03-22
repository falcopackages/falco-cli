:image: https://raw.githubusercontent.com/Tobi-De/falco/main/assets/og-image.jpg
:description: The packages and tools that comes included with a project generated with falco.

Packages and Tools
==================

This section provides an overview of the primary packages and tools, along with some of the design choices incorporated
into a project generated with **Falco**.

Let's start with the straightforward components, about which there isn't much to elaborate:

- `environs <https://github.com/sloria/environs>`_: Used for configuring settings via environment variables.
- `django-allauth <https://github.com/pennersr/django-allauth>`_: Handles login and signup processes.
- `Amazon SES <https://aws.amazon.com/ses/?nc1=h_ls>`_ and `Anymail <https://github.com/anymail/django-anymail>`_: Amazon SES is used for production email, facilitated by Anymail.
- `Docker <https://www.docker.com/>`_ and `s6-overlay <https://github.com/just-containers/s6-overlay>`_: Docker is configured for production, with s6-overlay enabling concurrent operation of ``django`` and ``django-q`` within a single container.
- `Sentry <https://sentry.io/welcome/>`_: Utilized for performance and error monitoring.
- `Whitenoise <https://whitenoise.evans.io/en/latest/>`_: Used to serve static files.
- `pre-commit <https://github.com/pre-commit/pre-commit>`_: Integrated by default to identify simple issues before pushing code to remote.
- `django-browser-reload <https://github.com/adamchainz/django-browser-reload>`_: Automatically reloads your browser on code changes in development.


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




.. _hatch: https://hatch.pypa.io/latest/
.. _django-template-partials: https://github.com/carltongibson/django-template-partials
.. _htmx: https://htmx.org/
.. _django-htmx: https://github.com/adamchainz/django-htmx
.. _dj-notebook: https://github.com/pydanny/dj-notebook
.. _tailwindcss: https://tailwindcss.com
.. _django-tailwind-cli: https://github.com/oliverandrich/django-tailwind-cli

