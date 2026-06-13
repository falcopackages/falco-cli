
:description: Here is the guide on how to install the falco's cli.

Installation
============

Falco CLI is available on PyPI and can be installed with uv or pip.

.. tabs::

  .. tab:: uv

    .. code-block:: shell

        uv tool install falco-cli

  .. tab:: pip

    .. code-block:: shell

        pip install falco-cli

Add ``falco_cli`` to your ``INSTALLED_APPS`` in your Django settings file:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'falco_cli',
        ...
    ]
