CRUD for your model
===================

Accelerate prototyping with basic CRUD (Create, Read, Update, Delete) python views and HTML templates, enhanced with htmx and Tailwind CSS.

crud
----

.. cappa:: falco.commands.ModelCRUD

This command generates htmx-powered create, read, update, and delete views for your model. It follows a similar idea
as `neapolitan <https://github.com/carltongibson/neapolitan>`_, but with a completely different approach. Instead of inheriting
from a class as done with `neapolitan`, this command generates basic `views`, `urls`, and HTML `templates`, and updates or overrides the
corresponding files in your project. I prefer this approach because, at the end, you'll have all the new code directly in front of you. It's easily
accessible and you can update it as you see fit. The idea is to accelerate project prototyping. Write a model and you instantly have views ready for it.


.. admonition:: Why function based views?
    :class: hint dropdown

    I think class-based views get complex faster than function-based views. Both have their use cases, but function-based views
    stay simpler to manage longer in my experience. There is an excellent document on the topic, read this `django views the right way <https://spookylukey.github.io/django-views-the-right-way/>`_.

If you want to see an example of the generated code, check out the `source code of the demo project <https://github.com/Tobi-De/falco/tree/main/demo/products.>`_.

Python code
^^^^^^^^^^^

All Python code added by this command will be in **append** mode, meaning it won't override the content of your existing files.
Instead, it will add code at the end or create the files if they are missing. The files that will be modified
are ``forms.py``, ``urls.py``, and ``views.py``. For brevity, I'll only show an example of what the `urls.py` file
might look like for a model named ``Product`` in a django app named ``products``.

.. code-block::bash

    falco crud product.products

.. literalinclude:: ../../demo/products/urls.py

As you can see, the convention is quite simple: ``<model_name_lower>_<operation>``. Note that if you don't specify the model name and run
``falco crud products``, the same code with the described conventions will be generated for all the models in the ``products`` app.
Now, if you're anything like me, the code above might have made you cringe due to the excessive repetitions of the term ``product``.
This wouldn't have been the case if the model was called `Category`, for example. For these specific cases, there is an ``--entry-point`` option.

Let's try it.

.. code-block:: bash

    falco crud product.products --entry-point

.. code-block:: python
    :caption: products/urls.py

    from django.urls import path

    from . import views

    app_name = "products"

    urlpatterns = [
        path("", views.index, name="index"),
        path("create/", views.create, name="create"),
        path("<int:pk>/", views.detail, name="detail"),
        path("<int:pk>/update/", views.update, name="update"),
        path("<int:pk>/delete/", views.delete, name="delete"),
    ]

Much cleaner, specifying that option means you consider the ``Product`` model as the entry point of your ``products`` app.
So, instead of the base URL of the app looking like "products/products/", it will just be "products/", assuming you registered your URLs in
your root URL config like this:

.. code-block:: python
    :caption: config/urls.py
    :linenos:
    :emphasize-lines: 4

    urlpatterns = [
    path("admin/", admin.site.urls),
    ...
    path("products/", include("products.urls", namespace="products"))
    ]

.. important::

    Currently, the root ``urls.py`` file is not automatically updated, so you need to do this manually.


HTML templates
^^^^^^^^^^^^^^

Unlike the Python code, the generated HTML templates will overwrite any existing ones. If you want to avoid this, you should commit
your changes before running this command or use the ``--only-python`` option to generate only Python code. The files are generated
with minimal styling (using Tailwind CSS) and are reasonably presentable.
Four files are generated:

* ``<model_name_lower>_list.html``
* ``<model_name_lower>_create.html``
* ``<model_name_lower>_detail.html``
* ``<model_name_lower>_update.html``

There is no ``<model_name_lower>_delete.html`` file because deletion is handled in the ``<model_name_lower>_list.html``.
Each generated HTML file expects to extend from a ``base.html`` template. Therefore, make sure you have a top-level ``base.html`` file in
your templates directory.


.. note::

    If you use the ``--entry-point`` option, the files will be named ``index.html``, ``create.html``, ``detail.html``, and ``update.html``.

To determine where to place the generated files, we check the ``DIRS`` key in the ``TEMPLATES`` settings of your Django project.
If it is populated, we take the first value in the list and generate the template files in ``<templates_dir>/<app_label>``.
If it is not populated, we use the classic Django layout, which is ``<app_label>/templates/<app_label>``. If you want an overview
of what the templates look like, check out the `demo project <https://github.com/Tobi-De/falco/tree/main/demo/templates/products>`_.

Examples
^^^^^^^^

Some usage examples.

.. code:: bash

    $ falco crud products.product
    $ falco crud products
    $ falco crud products.product -e="secret_field1" -e="secret_field2"
    $ falco crud products.product --only-html
    $ falco crud products.product --only-python
    $ falco crud products.product --entry-point


install-crud-utils
------------------

.. cappa:: falco.commands.InstallCrudUtils

These utilities may be imported by some parts of the code generated by the ``crud`` command. They are not installed simultaneously
with the ``crud`` command because you only need to run this once. Running this for each execution of the ``crud`` command would not
make sense. However, you can run this to update your code if the utilities have changed in **falco**. Like all ``crud`` related Python code,
the code is written in append mode, meaning it always adds to the end of the file if it already exists, and creates it if not.

**Determining the Destination for the File**

The command accepts an optional ``apps_dir`` argument. If this argument is not provided, the command will
use the name of the current directory and assume there's a subdirectory with the same name. For instance, if your Django
project root directory is named ``my_project``, the command will assume that there's a ``my_project`` subdirectory within the
current ``my_project`` directory. This is the default layout for projects generated by the `start-project </the_cli/start_project>`_ command.

The ``--output`` value, which defaults to ``core/utils.py``, is then appended to the ``apps_dir`` to determine the file's destination.
Following the previous example, the file will be written to ``myproject/my_project/core/utils``, where the first ``my_project`` is the root of your Django project.

If you decide to use the ``--output`` option to change the file's destination path (which defaults to ``core/utils.py``), you may need to adjust
some imports after executing the ``crud`` command.

Below is the content of the current ``utils.py``:

.. note::

    Rest assured, the comments won't be included in your final code.

.. literalinclude:: ../../src/falco_blueprints/crud/utils.py
