:layout: landing
:description: Falco is an opinionated toolkit for a modern Django development experience.


.. raw:: html

    <style>
    .yue img {
        margin-top: 0;
        margin-bottom: 0;
    }
    #head {
        display: flex;
        align-items: center;
        justify-content: space-between;
        column-gap: 20px;
    }

    @media (max-width: 600px) {
        #head {
            flex-wrap: wrap;
            justify-content: center;
        }
    }

    #head h1 {
        font-size: 4.2rem;
        margin-top: 3.4rem;
        margin-bottom: 1rem;
        font-weight: 700;
        line-height: 1.2;
    }
    </style>

   <div id="head">
        <img src="https://raw.githubusercontent.com/Tobi-De/falco/main/assets/falco-logo.svg" width=200 height=200>
        <div>
            <h1>Falco</h1>
            <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 3em;">
                <img src="https://github.com/Tobi-De/falco/actions/workflows/documentation.yml/badge.svg">
                <img src="https://github.com/Tobi-De/falco/actions/workflows/ci.yml/badge.svg">
                <img src="https://badge.fury.io/py/falco-cli.svg">
                <img src="https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg">
                <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json">
                <img src="https://img.shields.io/badge/license-MIT-blue.svg">
                <img src="https://img.shields.io/pypi/pyversions/falco-cli">
                <img src="https://img.shields.io/pypi/frameworkversions/django/falco-cli">
                <img src="https://img.shields.io/pypi/dm/falco-cli">
            </div>
        </div>
   </div>



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
