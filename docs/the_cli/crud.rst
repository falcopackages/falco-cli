CRUD for your model
===================

.. figure:: ../images/crud.svg

This command generates htmx-powered create, read, update, and delete views for your model. It follows a similar idea as `neapolitan <https://github.com/carltongibson/neapolitan>`_ 
but with a completely different approach. To use **neapolitan**, you'll inherit from its base class view, and for customization, get familiar with its API (which is fairly easy). 
I prefer function-based views, so this command generates basic and simple function-based views with some basic HTML templates.

.. admonition:: Why function based views?
    :class: hint dropdown

    Read this `django views the right way <https://spookylukey.github.io/django-views-the-right-way/>`_ article.