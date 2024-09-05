:layout: landing
:description: Falco is an opinionated toolkit for a modern Django development experience.

.. container::
    :name: home-head

    .. image:: /_static/falco-logo.svg
        :alt: Falco
        :width: 350
    

    .. container::

        .. raw:: html

            <h1>Falco</h1>

        .. container:: badges
           :name: badges

           .. image:: https://github.com/Tobi-De/falco/actions/workflows/ci.yml/badge.svg
              :alt: Github Actions Continuous Integration Status

           .. image:: https://github.com/Tobi-De/falco/actions/workflows/publish.yml/badge.svg
              :alt: Github Actions Publish Status

           .. image:: https://readthedocs.org/projects/falco-cli/badge/?version=latest&style=flat
              :alt: Documentation Status

           .. image:: https://badge.fury.io/py/falco-cli.svg
              :alt: PyPI Version

           .. image:: https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg
              :alt: Hatch Version

           .. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
              :alt: Ruff Version

           .. image:: https://img.shields.io/badge/license-MIT-blue.svg
              :alt: MIT License

           .. image:: https://img.shields.io/pypi/pyversions/falco-cli
              :alt: Supported Python Versions

           .. image:: https://img.shields.io/pypi/frameworkversions/django/falco-cli
              :alt: Supported Django Versions

           .. image:: https://img.shields.io/pypi/dm/falco-cli
              :alt: PyPI Downloads



.. rst-class:: lead

    Falco is your Django toolkit for faster prototyping and deployment of your Django projects. It offers commands for :doc:`project generation <the_cli/start_project/index>`,
    :doc:`CRUD view generation <the_cli/crud>`, :doc:`guides <guides/index>` that address common web development challenges tailored to Django and much more.

.. container:: buttons

    :doc:`Docs <install>`
    `Usage / Overview <the_cli/usage.html>`_
    `GitHub <https://github.com/tobi-de/falco>`_



.. grid:: 1 1 2 3
    :class-row: surface
    :padding: 0
    :gutter: 2

    .. grid-item-card:: :octicon:`terminal` The CLI
      :link: the_cli/index
      :link-type: doc

      The documentation for the falco command line interface (CLI).

    .. grid-item-card:: :octicon:`book` Guides
      :link: guides/index
      :link-type: doc

      A collection of guides on common web development topics and how to address them in django.

    .. grid-item-card:: :octicon:`history` Changelog
      :link: changelog
      :link-type: doc

      Explore the latest updates and the change history of the Falco project.

    .. grid-item-card:: :octicon:`comment-discussion` Discussion
      :link: https://github.com/tobi-de/falco/discussions

      Provide suggestions for improving the guides and share new ideas.

    .. grid-item-card:: :octicon:`alert-fill` Issue
      :link: https://github.com/tobi-de/falco/issues

      Use this section to report bugs and request new features for the CLI.

    .. grid-item-card:: :octicon:`people` Contributing
      :link: contributing
      :link-type: doc

      Learn how to contribute to the Falco project.

-----

.. raw:: html

    <h2>Contributors</h2>

.. include:: ../README.md
    :parser: myst_parser.sphinx_
    :start-after: <!-- contributors:start -->
    :end-before: <!-- contributors:end -->

.. toctree::
    :caption: Getting started
    :hidden:

    install
    the_cli/index
    guides/index

.. toctree::
    :caption: Development
    :hidden:

    contributing
    codeofconduct
    license
    changelog
