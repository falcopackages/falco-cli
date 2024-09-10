:description: A demonstration of the essential workflow of the Falco CLI, from generating a new project to creating CRUD views for a model.

Usage / Overview
================

This page outlines the optimal workflow for the initial setup of a project using the Falco CLI. This includes creating a new project,
initializing a Django application, adding a model, and generating CRUD views for the model.
This workflow represents the expected experience for a new Falco CLI user. If you encounter any issues reproducing this workflow,
please create a `new issue <https://github.com/Tobi-De/falco/issues/new>`_.


.. admonition:: Pre-requisites
    :class: important

    Make sure you have all the required tools installed as mentioned in the `installation page </install.html>`_.

Let's create a new project called **myjourney**. This will be a journaling app and its main app will be **entries**.
Each **entry** represents a journal entry within the **myjourney** app.

**1. Generate a new project and cd (change directory) into it**

.. code-block:: bash

    falco start-project myjourney && cd myjourney

**2. Project setup**

Refer to the ``justfile`` in the root of the project to understand the available commands. The command below sets up your
virtual environment using ``hatch`` (default, dev, and docs), runs the project migrations, creates a superuser
with ``admin@localhost`` as the email and ``admin`` as the password, and runs project linting with ``pre-commit``.

.. code-block:: bash

    just setup

At this point, you can run ``just server`` to start the project. While the UI may be basic (which I hope to improve in the future),
you have a fully functional ready to deploy django project. If you update the content of the home page, your browser will automatically reload.

**3. Create the new app, entries**

.. code-block:: bash

    just falco start-app entries

**4. Add some fields to your Entry model**

.. literalinclude:: /_static/snippets/entry_model.py

**5.  Make migrations for the new model and run them**

.. code-block:: bash

    just mm && just migrate

``mm`` is an alias for ``makemigrations``

.. admonition:: Auto migrations
    :class: tip dropdown

    It is highly probable that you will always need to run these commands after adding a new model, or just before
    executing ``crud`` (the next step). For this reason, there is an option to instruct the ``crud`` command to always
    perform this step first:

    .. code-block:: toml

        [tool.falco.crud]
        always-migrate = true

**6. Generate CRUD views for the Entry model**

.. code-block:: bash

    just falco crud entries.entry --entry-point --skip-git-check

Without the ``--skip-git-check`` option, the command will fail since we currently have some uncommitted changes in our repository.

**7. Run the project**

.. code-block:: bash

    just server

Now, check out http://127.0.0.1:8000/entries to see your running app.


.. todo::

    Add screenshots (or gif) or a walkthrough of the process and the resulting running app here.

