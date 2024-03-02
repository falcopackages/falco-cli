:image: https://raw.githubusercontent.com/Tobi-De/falco/main/assets/og-image.jpg
:description: Things that does not deserve a full guide or I don’t know where to put them.

Tips and extra
==============

This section contains miscellaneous tips and extras that don't warrant a full guide or don't fit elsewhere.

Understanding django Settings
-----------------------------

If there is a setting in ``settings.py`` or elsewhere that you don’t understand, go to the `official django settings reference page <https://docs.djangoproject.com/en/dev/ref/settings/>`__
and press Ctrl + F to search for it. I find this faster than using the search box on the Django documentation site.


Create superuser from environment variables
-------------------------------------------

You can easily create a Django superuser using environment variables. This is a convenient option of the ``createsuperuser``
command, and works with the ``--no-input`` flag. This is especially useful for creating a superuser without being prompted,
for example as part of your production server setup process. For more details on this, read the ``createsuperuser`` `command documentation <https://docs.djangoproject.com/en/dev/ref/django-admin/#django-admin-createsuperuser>`_.

.. code-block:: text
    :caption: In your OS environment variables or a .env file

    DJANGO_SUPERUSER_EMAIL=your_email@example.com
    DJANGO_SUPERUSER_PASSWORD=a_secure_password

You can set these environment variables on your local computer to easily create the same superuser with the same credentials for all your projects for your development needs.

.. code-block:: bash
    :caption: Create a superuser

    python manage.py createsuperuser --no-input

Local email testing
--------------------

If you're seeking a local SMTP client with a nice user interface for email testing, I suggest using `mailpit <https://github.com/axllent/mailpit>`_.
To integrate it into your project, you'll need to modify your ``settings.py`` as follows:

.. code-block::
    :caption: settings.py

    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend",
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1025


Lifecycle not signals
---------------------

I've come to fall in love with `django-lifecycle <https://github.com/rsinger86/django-lifecycle>`_ and their approach to hooking into
your Django objects' lifecycle. Traditionally, the way of dealing with this in Django is using `signals <https://docs.djangoproject.com/en/dev/topics/signals/>`_. Even
though there is a lot of criticism on using signals in the community, I think they can be particularly useful in certain scenarios (e.g: implementing a plugin system). However, one scenario where they are not beneficial in my humble opinion is in
organizing business logic. In such cases, I personally favor ``django-lifecycle`` because it follows the django ``fat models`` approach (essentially business logic in models).

Here is an example of using ``django-lifecycle`` straight from their README:

.. code-block:: python

    from django_lifecycle import LifecycleModel, hook, BEFORE_UPDATE, AFTER_UPDATE


    class Article(LifecycleModel):
        contents = models.TextField()
        updated_at = models.DateTimeField(null=True)
        status = models.ChoiceField(choices=['draft', 'published'])
        editor = models.ForeignKey(AuthUser)

        @hook(BEFORE_UPDATE, when='contents', has_changed=True)
        def on_content_change(self):
            self.updated_at = timezone.now()

        @hook(AFTER_UPDATE, when="status", was="draft", is_now="published")
        def on_publish(self):
            send_email(self.editor.email, "An article has published!")


Better user personal info fields
--------------------------------


Instead of using ``first_name`` and ``last_name`` when requesting personal information from your users, consider using ``full_name`` and ``short_name``.
These two fields can accommodate almost all naming patterns in the world, unlike the first two. If you want more details on why,
`watch this <https://youtu.be/458KmAKq0bQ?si=OgGblV_p2R3zdnoW>`_. One thing I would add is that if your target audience is very narrow, geographically based,
and unlikely to change or expand, then use whatever makes sense for them, even ``first_name`` and ``last_name``.

.. Avoid huge apps for large projects
.. ----------------------------------

Type Hinting
------------

These days, I hardly write Django projects without implementing some level of type hinting. However, resources on this topic specific to Django are quite rare.
A good starting point is the `FAQ section <https://github.com/typeddjango/django-stubs#faq>`_ of the django-stubs README. It provides sufficient information to
navigate through most common use cases. Since I don't overuse type hinting, I find it more than enough.

Generate admin
--------------

`django-extensions <https://django-extensions.readthedocs.io/en/latest/admin_generator.html>`_ has become a must-have in all of my projects, and one of my
favorite features is the ``admin-generator`` command. It generates code for your ``admin.py`` file based on your models. Here's how to use it:

.. code-block:: bash

    python manage.py admin_generator your_app | tail -n +2 > your_project/your_app/admin.py

.. note::

    The ``tail -n +2`` part is used to remove the first line of the generated file. This line, ``# -*- coding: utf-8 -*-``, sets the file encoding.
    However, it's largely unnecessary these days, unless you're coding in Python 2, which I sincerely hope is not the case.


As a hatch script

.. code-block:: toml

    [tool.hatch.envs.default.scripts]
    admin = "python manage.py admin_generator {args} | tail -n +2 > your_project/{args}/admin.py"


Auto Fill forms
---------------

Manually filling out forms during development can become annoying quickly, checkout `fakefiller <https://fakefiller.com/>`_.


Find Path Declaration for a View
--------------------------------

Sometimes, you might need to find the path associated with a specific view. Instead of navigating to your ``urls.py`` file and searching for the
view (for example, using ``CTRL + F``), there's a simpler and faster method. You can use the common `jump to usage/jump to declaration` feature available in most IDEs.
In PyCharm, for instance, it's ``CTRL + B``.

This technique enables you to jump directly to the usage of the view. Since you typically use the function only once and that's usually in your ``urls.py``, it will lead
you directly to the associated path. This tip might seem obvious to some, but it took me a while to figure it out. So, I'm sharing it for those who might not be aware of this.

Navigating Project URLs with Django-Extensions
----------------------------------------------

    "✨ If you use #django and don't know about django-extensions' `show_url` management command, it's the cheatsheet you didn't know you needed... or you knew you needed but didn't know what/where to look for it at.
    It saves me tons of time and frustration when figuring out what a view is named from a third party app."

    -- `Jeff Triplett <https://mastodon.social/@webology/110271223054909764>`_

.. code-block:: bash
    :caption: usage example

    python manage.py show_urls # show all urls in the project
    python manage.py show_urls | grep allauth # show all urls for allauth
