:image: https://raw.githubusercontent.com/Tobi-De/falco/main/assets/og-image.jpg
:description: A guide on how to write documentation for python/django software projects.

Writing documentation
=====================

https://github.com/testthedocs/awesome-docs

.. warning::

    Work in progress. To receive updates `subscribe to this discussion <https://github.com/Tobi-De/falco/discussions/39>`_ or
    follow me on `x <https://twitter.com/tobidegnon>`_ or `mastodon <https://fosstodon.org/@tobide>`_.

Intro

Documentation Frameworks
------------------------


Markdown and reStructuredText
-----------------------------

https://github.github.com/gfm/

https://myst-parser.readthedocs.io/en/latest/

https://sphinx-intro-tutorial.readthedocs.io/en/latest/

Python documentation tools
--------------------------

This template does not include a documentation setup, but it is very important for most projects (at least it should be)
to have a documentation site, especially if you are not working alone. Here are the options I would suggest for setting
up a documentation, recently I tend to favor the first one.

-  `Mkdocs <https://www.mkdocs.org/>`__ with the `Material theme <https://squidfunk.github.io/mkdocs-material/getting-started/>`__
-  `Sphinx <https://www.sphinx-doc.org/en/master/>`__ with the `Furo theme <https://github.com/pradyunsg/furo>`__

There is a chance that in the future I will include the docs directly in the template but for now here is a quick guide to
configure mkdocs with the material theme:

Sphinx
^^^^^^

Installation and configuration
++++++++++++++++++++++++++++++

Deploy your documentation
+++++++++++++++++++++++++++++


MkDocs
^^^^^^

Installation and configurations
+++++++++++++++++++++++++++++++

Copy the configuration below into your ``pyproject.toml`` file under the ``[tool.poetry.dependencies]`` section.

.. code:: toml

   [tool.poetry.group.docs]
   optional = true

   [tool.poetry.group.docs.dependencies]
   mkdocs = "^1.4.2"
   mkdocs-material = "^8.5.10"
   mkdocs-material-extensions = "^1.1.1"
   mkdocs-include-markdown-plugin = "3.9.1"

Install the new dependencies.

.. code:: shell

   poetry install --with docs

Create your new **mkdocs** site.

.. code:: shell

   mkdocs new .

Update the ``mkdocs.yml`` file to specify the **material** theme, your configuration should look like this:

.. code:: yaml

   site_name: My Docs # change this to the name of your project
   theme:
     name: material

Run the documentation site locally

.. code:: shell

   mkdocs serve

If you noticed, the dependencies added above via the section ``[tool.poetry.group.docs.dependencies]`` include more than just
mkdocs and the material theme, specifically :

-  `mkdocs-material-extensions <https://github.com/facelessuser/mkdocs-material-extensions>`__: Markdown extension resources for MkDocs for Material
-  `mkdocs-include-markdown-plugin <https://github.com/mondeja/mkdocs-include-markdown-plugin>`__: Include other markdown files in your mkdocs site

For a complete example of how I configure them in projects, see this `configuration file <https://github.com/Tobi-De/dj-shop-cart/blob/master/mkdocs.yml>`__.

Deploy your documentation
+++++++++++++++++++++++++

**Mkdocs** can turn your documentation into a static site that you can host anywhere, `netlify <https://www.netlify.com/>`__, `github pages <https://pages.github.com/>`__, etc.
To build your site, run the command below and you will have a new ``site`` directory at the root of your project:

.. code:: shell

   mkdocs build

This folder contains everything that is necessary to deploy your static site.

If you choose the **github pages** route, you can automate the process with `github actions <https://github.com/features/actions>`__,
the official **mkdocs-material** documentation explains `how to do it <https://squidfunk.github.io/mkdocs-material/publishing-your-site/>`__.
To use github actions, you will probably need a ``requirements.txt`` file, you can generate one with only what is needed
to build the docs with the command below.

.. code:: shell

   poetry export -f requirements.txt --output docs/requirements.txt --without-hashes --only docs

Read the `mkdocs <https://www.mkdocs.org/>`__ and `mkdocs-material <https://squidfunk.github.io/mkdocs-material/getting-started/>`__ docs for more advanced configurations and details on what is possible.
