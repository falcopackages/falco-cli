:description: start a new django project ready for your next saas idea.

Start project
=============

.. cappa:: falco_cli.commands.StartProject

Initialize a new django project the falco way. This project-starter makes several assumptions; we'll go through the most important choices I made in the next couples of sections.
I'll list some alternatives below in case you don't agree with my choices. But even if you choose to use an alternative, most commands
can still be useful to you, and the `guides </guides/index.html>`_ are not particularly tied to the generated project. So, even with another project-starter, **Falco**
can still bring you value.


.. tabs::

  .. tab:: Tailwind CSS

    .. code-block:: shell

        falco start-project myproject

  .. tab:: Bootstrap CSS

    .. code-block:: shell

        falco start-project myproject -b bootstrap


.. note::

   The **authors** key of the ``[tool.project]`` section in the ``pyproject.toml`` is set using your git global user
   configuration. If you haven't set it yet, `see this page <https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup#_your_identity>`_.


.. admonition:: Experimental
  :class: important

  You can update your project to stay current with the latest changes in the project starter. Please note that this is an experimental feature. Ensure you commit your
  changes before running the command. If there are conflicts, ``.rej`` files will be generated, which you will need to review and manually update the corresponding files
  if necessary.

  .. code-block:: shell

    falco update-project


The subsequent sections will delve deeper into the folder structure, package choices, and provide guidance on deploying your project.

Alternative starters
--------------------

Here are some alternative project starters that you can consider if the falco starter is not to your liking:

- `cookiecutter-django <https://github.com/cookiecutter/cookiecutter-django>`_
- `django-twc-project <https://github.com/westerveltco/django-twc-project>`_
- `django-hatch-startproject <https://github.com/oliverandrich/django-hatch-startproject>`_
- `django-poetry-startproject <https://github.com/oliverandrich/django-poetry-startproject>`_
- `django-startproject <https://github.com/jefftriplett/django-startproject>`_
- `djangox <https://github.com/wsvincent/djangox>`_
- `wemake-django-template <https://github.com/wemake-services/wemake-django-template>`_


.. toctree::
    :hidden:

    structure
    dependency
    packages
    deploy
    issues


