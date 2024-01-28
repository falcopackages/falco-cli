:image: https://raw.githubusercontent.com/Tobi-De/falco/main/assets/falco-logo.svg
:description: A demonstration of the essential workflow of the Falco CLI, from generating a new project to creating CRUD views for a model.

Usage / Overview
================

This page outlines the optimal workflow for the initial setup of a project using the Falco CLI. This includes creating a new project,
initializing a Django application, adding a model, and generating CRUD views for the model
This workflow represents the expected experience for a new Falco CLI user. If you encounter any issues reproducing this workflow,
please create a `new issue <https://github.com/Tobi-De/falco/issues/new>`_.

Let's create a new project called **myjourney**. This will be a journaling app and its main app will be **entries**.
Each **entry** represents a journal entry within the **myjourney** app.

**1. Generate a new project and cd (change directory) into it**

.. code-block:: bash

    falco start-project myjourney && cd myjourney

**2. Create a new virtual environment for the project and install dependencies**

.. code-block:: bash

    hatch shell


**3. Initialize git and install pre-commit hooks**

.. code-block:: bash

    git init && pre-commit install

If necessary, adjust the python_version value in the ``.pre-commit-config.yaml`` file.

**4. Create a new .env file**

.. code-block:: bash

    falco sync-dotenv

**5. Fill in some values for the admin user**

.. code-block:: text
    :caption: .env

    DJANGO_SUPERUSER_EMAIL=admin@mail.com
    DJANGO_SUPERUSER_PASSWORD=admin

**6. Migrate, and create the admin user**

.. code-block:: bash

    hatch run migrate && falco setup-admin

**7. Create the new app, entries**

.. code-block:: bash

    hatch run start-app entries && falco start-app entries

**8. Add some fields to your Entry model**

.. code-block:: python

    class Entry(TimeStampedModel):
        # the TimeStampedModel adds the fields `created` and `modified` so we don't need to add them
        title = models.CharField(max_length=255)
        content = models.TextField()
        created_by = models.ForeignKey("users.User", on_delete=models.CASCADE)


**9.  Make migrations for the new model and run them**

.. code-block:: bash

    hatch run makemigrations && hatch run migrate**

**10. Generate CRUD views for the Entry model**

.. code-block:: bash

    falco crud entries.entry --entry-point --skip-git-check

**11. Run the project**

.. code-block:: bash

    falco work

Now, check out http://127.0.0.1:8000/entries to see your running app.

This process currently requires 11 commands. Considering the outcome, it's not too shabby! However, I'm confident there's still plenty of room for improvement.
If you have any suggestions on how to improve this workflow, feel free to open a discussion at https://github.com/Tobi-De/falco/discussions.

.. todo::

    Add screenshots (or gif) or a walkthrough of the process and the resulting running app here.

