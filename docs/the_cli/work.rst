Running multiple process in parallel
====================================

.. warning::

   This command right now does not work as I was hoping it to. To make it work, you need to have the ``falco-cli`` installed in the same virtualenv as your
   project. I would prefer for that not to be the case, but right now I don't know how to fix it.


.. cappa:: falco.commands.Work


This command allows you to run multiple commands simultaneously. Typically, when working with a large or growing django project, you
reach a point where you need to run multiple processes to run your project. This might include a *Redis server*, a *Tailwind compile* command,
`a task queue worker </guides/task_queues_and_schedulers.html>`_, etc. With this command, you can run all these commands in parallel within a single terminal.
It execute the commands by reading your ``pyproject.toml`` file and running the commands defined in the ``[tool.falco.work]`` section.

.. There is a default configuration available when you generate your project with `start-project </the_cli/start_project.html>`_, and you can update it
.. as needed.
.. Here is the default configuration:

.. .. code:: toml

..    |[tool.falco.work]
..    server = "python manage.py migrate && python manage.py tailwind runserver"

.. And this is what a more advance configuration might looks like:

Here is an example of what a falco **work** configuration might looks like:

.. code:: toml

   [tool.falco.work]
   server = "python manage.py migrate && python manage.py tailwind runserver"
   redis = "redis-server"
   worker = "python manage.py qcluster"

Under the hood, this command utilizes `honcho <https://github.com/nickstenning/honcho>`_ to execute the defined commands, with each command running in its own separate process.

.. note::

   If no command is defined in the ``pyproject.toml`` file, the default behavior is to run the Django ``runserver`` command.

I was inspired by the `forge-work <https://www.forgepackages.com/docs/forge-work/>`_ package to create this command. It is a more powerful version of the one I have here.
The `forgepackages <https://github.com/forgepackages>`_ repository has some great tools for Django development in general. I would recommend checking them out as they might have something of interest to you.

This command runs in the foreground, so as soon as you kill the current terminal, all processes will be stopped. It is meant for development purposes only.
If you launch it and the Django server fails, indicating that the port is already in use, there is a chance that a previously running server was not properly killed
and is still running. To kill all previous running processes, run the following command:

.. code:: bash

   $ lsof -i :8000 -t | xargs -t kill # replace 8000 with the port you are using

This command was copied from this `blog post <https://adamj.eu/tech/2023/11/19/django-stop-backgrounded-runserver/>`_.
