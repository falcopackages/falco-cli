:image: https://raw.githubusercontent.com/Tobi-De/falco/main/assets/og-image.jpg
:description: Here is the guide on how to install the falco's cli.

Installation
============

Falco is available on PyPI and can be installed with pip or your favorite Python package manager.

.. code-block:: shell

    pip install falco-cli

You can also automatically install just with falco by running:

.. tabs::

  .. tab:: PIP

    .. code-block:: shell

        pip install "falco-cli[just]"

  .. tab:: PIPX

    .. code-block:: shell

        pipx install "falco-cli[just]"

  .. tab:: UV

    .. code-block:: shell

        uv tool install "falco-cli[just]"


.. note::

    The ``just`` extra does not work on Windows. If you are on Windows, you can follow the installation instructions
    `here <https://just.systems/man/en/chapter_4.html>`_

Next Up
-------

.. grid:: 1 1 1 2
    :class-row: surface
    :gutter: 2
    :padding: 0

    .. grid-item-card:: :octicon:`terminal` The CLI
      :link: the_cli/index
      :link-type: doc

      The documentation for the ``falco`` command line interface (CLI).

    .. grid-item-card:: :octicon:`book` Guides
      :link: guides/index
      :link-type: doc

      A collection of guides on common web development topics and how to address them in django.
