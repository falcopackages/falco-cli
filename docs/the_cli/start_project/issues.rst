:description: Common issues and solutions that you may encounter with a project generated with falco.

Known issues
============

Here is a collection of known issues and their solutions that you may encounter when running a falco project.


Permission denied on Tailwind CLI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you encounter an error similar to the one below when trying to run the server:

.. code-block:: bash

    08:12:38 tailwind | PermissionError: [Errno 13] Permission denied:
    08:12:38 tailwind | '/home/tobi/.local/bin/tailwindcss-linux-x64-3.4.10'

The simplest solution is to delete the file and re-run the server. The file will be re-downloaded, and the error should be resolved.

hatch-pip-compile
^^^^^^^^^^^^^^^^^

.. admonition:: 2024-03-04 Update
   :class: note

   I've recently tried the pip installation of Hatch (version 1.9.3), and the issues I was experiencing with hatch-pip-compile appear to be fully resolved.
   As a result, the binary is no longer a strict requirement, and the issue I describe below should no longer be a concern. However, there is still an advantage to
   using the binary version: updating hatch is a simple as running the following command:

   .. code-block:: bash

      hatch self update


In my experience, the hatch-pip-compile plugin may not function properly if hatch is not installed using a `binary <https://hatch.pypa.io/latest/install/#standalone-binaries>`_.
Therefore, ensure that you have the latest version of hatch (at least 1.8.0) and that you have installed it using the binary distribution.

hatch and pre-commit
^^^^^^^^^^^^^^^^^^^^

If you encounter an error when trying to make a commit after installing the pre-commit hooks, the error message may look like this:

.. code-block:: bash

   $ An unexpected error has occurred: PermissionError: [Errno 13] Permission denied: '/usr/local/hatch/bin/hatch' Check the log at /Users/tobi/.cache/pre-commit/pre-commit.log

To resolve this issue, you can change the owner of the hatch binary using the following command:

.. code-block:: bash

   $ sudo chown $USER /usr/local/hatch/bin/hatch

If you are unsure of the location of your hatch binary, you can use the following command to change the owner:

.. code-block:: bash

   $ sudo chown $USER $(which hatch)


pre-commit python version
^^^^^^^^^^^^^^^^^^^^^^^^^

If you encounter the following error:

.. code-block:: shell

   RuntimeError: failed to find interpreter for Builtin discover of python_spec='python3.11'

You need to update the section below (located at the beginning of the ``.pre-commit-config.yaml`` file) to match the Python version in your virtual environment:

.. code-block:: yaml

   default_language_version:
      python: python3.11 # TODO: Change this to match your virtual environment's Python version
