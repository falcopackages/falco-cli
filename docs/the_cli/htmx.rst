:image: https://raw.githubusercontent.com/Tobi-De/falco/main/assets/og-image.jpg
:description: A set of handy utilities for easily obtaining the htmx library and its extensions locally on your computer.

HTMX goodies
============

A set of handy utilities for easily obtaining the htmx library and its extensions locally on your computer.

htmx
----

.. cappa:: falco.commands.Htmx

Download the htmx javascript library. You won’t have to download htmx or its extensions often but at least if you need it, I think this
is an easy way to get the file available locally.
This command also utilizes your ``pyproject.toml`` file (if available) to store the path where the file was downloaded. This information is
saved in the ``[tool.falco]`` section. The purpose of this is to streamline future downloads: if you attempt to download the htmx file again,
it will recognize the existing path and update the existing file, eliminating the need for you to specify the path again.

Here is what this configuration looks like:

.. code-block:: toml

   [tool.falco]
   htmx = "path/to/htmx.min.js:1.9.10"

The value is a string that specifies the path to the file along with the version htmx. The version specification is optional. If you wish to modify this configuration
without mentioning the version, you can do so as follows:

.. code-block:: toml

   [tool.falco]
   htmx = "path/to/htmx.min.js"

Upon subsequent download, the configuration file will be updated with the version of the file.


htmx-ext
--------

This command downloads an htmx extension. The list of extensions is pulled from `htmx-extensions.oluwatobi.dev <https://htmx-extensions.oluwatobi.dev/>`_. If you run
the command without specifying any arguments, it will list all the available extensions instead.
Similar to the `htmx` commands, this will also use your ``pyproject.toml`` file if it's found. However,
it's solely for downloading the extensions file next to your ``htmx.min.js`` file, in case no path was specified in the command.

.. cappa:: falco.commands.HtmxExtension

**Example**

.. code-block:: bash

   falco htmx-ext sse
