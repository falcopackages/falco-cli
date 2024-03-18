:image: https://raw.githubusercontent.com/Tobi-De/falco/main/assets/og-image.jpg
:description: Run multiple commands in parallel to start your django project.

Work - Running multiple process in one session
==============================================

.. cappa:: falco.commands.Work


This command allows you to run multiple commands simultaneously. Typically, when working with a large or growing django project, you
reach a point where you need to run multiple processes to run your project. This might include a *Redis server*, a *Tailwind compile* command,
`a task queue worker </guides/task_queues_and_schedulers.html>`_, etc. With this command, you can run all these commands in parallel within a single terminal.
It execute the commands by reading your ``pyproject.toml`` file and running the commands defined in the ``[tool.falco.work]`` section.

Here is an example of what a falco **work** configuration might looks like:

.. code:: toml

   [tool.falco.work]
   server = "python manage.py migrate && python manage.py tailwind runserver"
   redis = "redis-server"
   worker = "python manage.py qcluster"

**Examples**

.. code-block:: bash

      falco work

You can customize the address of the Django server just like you would when running ``runserver`` directly

.. code-block:: bash

      falco work 127.0.0.1:8001
      falco work 8002

Under the hood, this command utilizes `honcho <https://github.com/nickstenning/honcho>`_ to execute the defined commands, with each command running in its own separate process.

.. note::

   If no command is defined in the ``pyproject.toml`` file, the default behavior is to run the Django ``runserver`` command.

I was inspired by the `forge-work <https://www.forgepackages.com/docs/forge-work/>`_ package to create this command. It is a more powerful version of the one I have here.
The `forgepackages <https://github.com/forgepackages>`_ repository has some great tools for Django development in general. I would recommend checking them out as they might have something of interest to you.

This command runs in the foreground, so as soon as you kill the current terminal, all processes will be stopped. It is meant for development purposes only.
If you launch it and the Django server fails, indicating that the port is already in use, there is a chance that a previously running server was not properly killed
and is still running. To kill all previous running processes, run the following command:

.. code:: bash

   $ lsof -i :8000 -sTCP:LISTEN -t | xargs -t kill # replace 8000 with the port you are using

This command was copied from this `blog post <https://adamj.eu/tech/2023/11/19/django-stop-backgrounded-runserver/>`_.
