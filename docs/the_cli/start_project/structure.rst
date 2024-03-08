:image: https://raw.githubusercontent.com/Tobi-De/falco/main/assets/og-image.jpg
:description: Files and forlder structure of project generated with falco.


Project Structure
=================

.. todo::

   I'm not satisfied with the current way this page is scructured and how things are explained.

Let's go through the basics of file structure and folders, so that you'll get an overview of what you're dealing with and don't feel completely lost or overwhelmed.
We won't go through the full levels of file structure, but just the essentials.

.github
-------

This directory is a GitHub-specific folder, meant for configurations related to GitHub like bots, GitHub Actions workflows, etc.
At the root of the folder, you'll see a ``dependabot.yml`` file. It is a config file for `Dependabot <https://github.com/dependabot>`_ that is configured to
check weekly for dependency upgrades in your requirements files (more on that in the virtualenv management section). 
There is a workflow directory with a ``ci.yml`` file (CI stands for `Continuous Integration <https://en.wikipedia.org/wiki/Continuous_integration>`_). 
This file is meant to run tests, deployment checks, and type checks every time you push a new commit to GitHub to make sure nothing has broken 
from the previous commit (assuming you do write tests).

docs
----

This folder is meant to house the documentation for your projects. The documentation uses a basic `sphinx <https://www.sphinx-doc.org/en/master/>`_ setup with the `furo <https://github.com/pradyunsg/furo>`_ theme. 
There is a basic structure in place that encourages you to structure your documentation based on your `django applications <https://docs.djangoproject.com/en/dev/ref/applications/>`_. 
By default, you are meant to write using `reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_, but the `myst-parser <https://myst-parser.readthedocs.io/en/latest/>`_ is configured so 
that you can use `markdown <https://www.markdownguide.org/>`_. Even if you are not planning to have very detailed and highly structured documentation (for some ideas on that, check out the `documentation writing guide </guides/writing_documentation.html>`_), 
it can be a good place to keep notes on your project architecture, setup, external services, etc. It doesn't have to be optimal to be useful.

 "The Palest Ink Is Better Than the Best Memory."

 --- Chinese proverb

project_dir
-----------

This is the core of your project. It contains all the essentials of your Django project: ``settings``, ``root urls``, ``applications``, ``templates``, and ``static``. Every 
piece of code meant for the main project goes in there. It is very close to the default Django layout. The main difference is that when 
you run the Django ``startapp`` command, it puts new apps in the root directory. That's why Falco comes with its own ``start-app`` command that
will move new apps to the ``project_dir`` and automatically register them in your settings ``INSTALLED_APPS``.

deploy
------

This folder contains the essentials for your project deployment. More details can be found in the `deployment </the_cli/start_project/deploy.html>`_ section.

tests
-----

This folder is where you write your tests. It can follow the same structure as your Django project, with a new tests folder 
for each application, or you can have one ``tests`` folder per application directory.

-----

Here is an overview of the complete file structure of a generated project:

.. figure:: ../../images/project-tree.svg