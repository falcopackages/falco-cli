:layout: landing
:image: https://raw.githubusercontent.com/Tobi-De/falco/main/assets/og-image.jpg
:description: Falco is an opinionated toolkit for a modern Django development experience.

.. container::
    :name: home-head

    .. image:: https://raw.githubusercontent.com/Tobi-De/falco/main/assets/falco-logo.svg
        :alt: Falco
        :width: 400
        :height: 400

    .. container::

        .. raw:: html

            <h1>Falco</h1>

        .. container:: badges
           :name: badges

           .. image:: https://github.com/Tobi-De/falco/actions/workflows/documentation.yml/badge.svg

           .. image:: https://github.com/Tobi-De/falco/actions/workflows/publish.yml/badge.svg

           .. image:: https://badge.fury.io/py/falco-cli.svg

           .. image:: https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg

           .. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json

           .. image:: https://img.shields.io/badge/license-MIT-blue.svg

           .. image:: https://img.shields.io/pypi/pyversions/falco-cli

           .. image:: https://img.shields.io/pypi/frameworkversions/django/falco-cli

           .. image:: https://img.shields.io/pypi/dm/falco-cli



.. rst-class:: lead

    Falco is a Django toolkit that improves development with commands for project initiation, CRUD view generation, and
    guides addressing common web development issues tailored to Django.


.. container:: buttons

    `Docs </install.html>`_
    `GitHub <https://github.com/tobi-de/falco>`_


.. grid:: 1 1 2 3
    :class-row: surface
    :padding: 0
    :gutter: 2

    .. grid-item-card:: :octicon:`terminal` The CLI
      :link: /the_cli/

      The documentation for the falco command line interface (CLI).

    .. grid-item-card:: :octicon:`book` Guides
      :link: /guides/

      A collection of guides on common web development topics and how to address them in django.

    .. grid-item-card:: :octicon:`history` Changelog
      :link: /changelog.html

      Explore the latest updates and the change history of the Falco project.

    .. grid-item-card:: :octicon:`comment-discussion` Discussion
      :link: https://github.com/tobi-de/falco/discussions

      Provide suggestions for improving the guides and share new ideas.

    .. grid-item-card:: :octicon:`alert-fill` Issue
      :link: https://github.com/tobi-de/falco/issues

      Use this section to report bugs and request new features for the CLI.

    .. grid-item-card:: :octicon:`people` Contributing
      :link: /contributing.html

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
