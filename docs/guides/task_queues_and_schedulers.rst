:image: https://raw.githubusercontent.com/Tobi-De/falco/main/assets/og-image.jpg
:description: Offload tasks in django using task queues and periodic tasks using schedulers.

Task Queues and Schedulers
==========================

Task queues
-----------

Task queues are used to offload tasks to a dedicated worker process when the processing of those tasks does not fit into a traditional request-response cycle.
In other words, if you need to do something that might take too long to process and whose result does not need to be shown immediately to the user, you use a queue manager.

Think of it as your Django application having an assistant. When a task is too time-consuming to be handled instantly, it's assigned to the assistant for completion, allowing your app to continue
functioning normally and serving your clients. Once the assistant completes the task, it returns the result to your django app.

.. admonition:: Example

        .. image:: ../images/task_queue.png


        1. A user uploads a large excel file to your web application for processing.
        2. The Django app immediately returns a **processing...** message to avoid blocking.
        3. The Django project adds the task to a broker (`redis <https://redis.io/>`_, `rabbitmq <https://www.rabbitmq.com/>`_, database, etc.), a service used to store tasks that need processing.
        4. Another process, the worker, retrieves the task from the broker and processes it.
        5. The worker process the task.

        There is a final step not shown in the diagram due to clutter. In this step, through some form of callback mechanism,
        the worker notifies the Django app that it has completed its work and sends back the result. How this callback mechanism works
        depends on the tool you choose for the task queue implementation.


Task scheduling
---------------

Schedulers are used to periodically execute tasks. They assist in scheduling tasks to run at specific times or intervals. For instance,
if you need to send an email to your users every day at 8:00 AM, a scheduler can be used for this purpose. While this can also be achieved using
a cron job, which is a common approach, most task queues also provide a scheduler. If task scheduling is all you need, a simple and straightforward
option is to use `cron jobs <https://cronitor.io/guides/cron-jobs>`_ in combination with custom `django management commands <https://docs.djangoproject.com/en/5.0/howto/custom-management-commands/>`_ (or `job scheduling from django-extensions <https://django-extensions.readthedocs.io/en/latest/jobs_scheduling.html>`_).
The Django management command would contain the code to, for example, send the email to users, and the crontab would execute the command at the specified schedule.

Popular packages options
------------------------

There are many options available in the `django third-party ecosystem <https://djangopackages.org/grids/g/workers-queues-tasks/>`__, some focus solely on providing a task queue,
others are just schedulers and many of them provide both in one package. You can also search for purely python solutions and
integrate them into your django project yourself.

I prefer options that do not require additional infrastructure (redis, rabbitmq, etc.) for simple tasks. For instance, solutions that can leverage any existing database setup I have.
For more complex tasks, I tend to choose a solution that supports redis as a task broker.

.. admonition:: My pick in the list below
        :class: note dropdown

        My current pick in this list is **django-q2**. It is a fork of the original **django-q** project, which is no longer maintained.
        Here is an example of using ``django-q2`` to run a task in background:

        .. code-block::
                :caption: views.py
                :linenos:
                :emphasize-lines: 7

                from django_q.tasks import async_task

                def long_running_task(user_id):
                        ...

                def my_view(request):
                        task_id = async_task(long_running_task, user_id=request.user.id)
                        ...

        The ``async_task`` function returns instantly, as it doesn't directly execute the ``long_running_task`` function.
        Instead, it delegates the function to a worker for execution. To initiate this worker process (which also includes a scheduler),
        you need to open a new terminal and execute the following command:

        .. code-block:: shell

                python manage.py qcluster

        Couldn't get much easier than this, right? :)


+-------------------+----------------------------------------------------+------------+------------+-----------------------------+
| Package           | Repository URL                                     | Task Queue | Scheduler  | Requires External Service?  |
+===================+====================================================+============+============+=============================+
| django-q2         | https://github.com/GDay/django-q2                  | Yes        | Yes        | No                          |
+-------------------+----------------------------------------------------+------------+------------+-----------------------------+
| wakaq             | https://github.com/wakatime/wakaq                  | Yes        | Yes        | Yes                         |
+-------------------+----------------------------------------------------+------------+------------+-----------------------------+
| django-pgpubsub   | https://github.com/Opus10/django-pgpubsub          | Yes        | No         | No                          |
+-------------------+----------------------------------------------------+------------+------------+-----------------------------+
| rocketry          | https://github.com/Miksus/rocketry                 | No         | Yes        | No                          |
+-------------------+----------------------------------------------------+------------+------------+-----------------------------+
| schedule          | https://github.com/dbader/schedule                 | No         | Yes        | No                          |
+-------------------+----------------------------------------------------+------------+------------+-----------------------------+
| django-dramatiq   | https://github.com/Bogdanp/django_dramatiq         | Yes        | No         | Yes                         |
+-------------------+----------------------------------------------------+------------+------------+-----------------------------+
| django-rq         | https://github.com/rq/django-rq                    |            |            |                             |
|                   |                                                    | Yes        | Yes        | Yes                         |
|                   | https://github.com/dsoftwareinc/django-rq-scheduler|            |            |                             |
+-------------------+----------------------------------------------------+------------+------------+-----------------------------+
| procrastinate     | https://github.com/procrastinate-org/procrastinate | Yes        | Yes        | No                          |
+-------------------+----------------------------------------------------+------------+------------+-----------------------------+
| celery            | https://github.com/celery/celery                   | Yes        | Yes        | Yes                         |
+-------------------+----------------------------------------------------+------------+------------+-----------------------------+

.. admonition:: Auto reload in development
    :class: dropdown

    If you are using one of these you might want an automatic reload feature when files changes in dev, you can use the ``hupper``
    python package for that purpose. It watches for file changes in the current directory and restarts the worker process automatically.

    .. code-block:: bash
        :caption: usage example

        hupper -m django_q.cluster

Basic django-q2 configuration
-----------------------------

.. tabs::

  .. tab:: Using the database as broker

    .. code-block:: python
        :caption: settings.py

        Q_CLUSTER = {
            "name": "DjangORM",
            "workers": 4,
            "timeout": 90,
            "retry": 120,
            "queue_limit": 50,
            "bulk": 10,
            "orm": "default",
            "catch_up": False,
        }


  .. tab:: Using redis as broker

    .. code-block:: python
        :caption: settings.py

        CACHES = {"default": env.cache("REDIS_URL")}

        # This configuration assumes that Redis is configured for caching in a similar way as described above.
        Q_CLUSTER = {
            'name': 'DJRedis',
            'workers': 4,
            'timeout': 90,
            'django_redis': 'default'
        }


Deployment with a task queue
----------------------------

Deploying a Django project that uses a task queue is not as straightforward, but still relatively simple. At this point, I hope you've
understood that running a task queue or task schedulers implies running another process (the worker) in addition to your django server.
You can have one process for the task queues and another for the schedulers, but usually, with most packages, you can have both in one process with one command.
For example, if you chose ``django-q2``, all you need to run is:

.. code-block:: shell

        python manage.py qcluster

This command will enable both the task queue and scheduling capabilities. If you are running your Django app on a Linux server, the most common option is to have a
process manager to run and manage both your Django server and the worker process, or any other processes your Django project needs. The two most popular options
are `systemd <https://systemd.io/>`_ and `supervisord <http://supervisord.org/>`_. Systemd is natively available on most Linux distributions, but you need to install Supervisor.
In my experience, there are no real advantages of one over the other, so I would advise just picking one; either will be fine.

Here are some basic configuration examples. Please note that the code provided only concerns the worker process.

.. tabs::

        .. tab:: Systemd

                .. code-block:: text
                        :caption: supervisord.conf

                        [Unit]
                        Description=Your Django Qcluster Worker

                        [Service]
                        WorkingDirectory=/path/to/your/project
                        ExecStart=/path/to/your/venv/bin/python manage.py qcluster
                        User=your_username
                        Group=your_groupname
                        Restart=always
                        StandardOutput=append:/var/log/your_project/qcluster.out.log
                        StandardError=append:/var/log/your_project/qcluster.err.log

                        [Install]
                        WantedBy=multi-user.target


        .. tab:: Supervisord

                .. code-block:: text
                        :caption: worker.service

                        [program:your_project_qcluster]
                        command=/path/to/your/venv/bin/python manage.py qcluster
                        directory=/path/to/your/project
                        user=your_username
                        group=your_groupname
                        autostart=true
                        autorestart=true
                        stderr_logfile=/var/log/your_project_qcluster.err.log
                        stdout_logfile=/var/log/your_project_qcluster.out.log


If you are running your project with Docker, the process is the same. You need to have another Dockerfile in addition to your main one.
This Dockerfile is practically identical, but with the entry command running the worker process (e.g., ``python manage.py qcluster``)
instead of your Django application server. There is also a simple alternative to run both the Django process and the worker in a single container.
For more on that, read the guide on `running your project in a single container </guides/running_project_in_a_container.html>`_.

On the other hand, if you are running your project on a platform as a service (PAAS), they usually have a way to declare a worker process.
For example, Heroku (and most PAAS that use a Procfile) have a straightforward way to declare a worker process in the Procfile.

Here is an example of what that looks like with Heroku:

.. code-block:: text
        :caption: Procfile

        web: gunicorn myproject.wsgi
        worker: python manage.py qcluster

The End
-------

In conclusion, this guide aimed to provide enough information for you to understand and choose a task queue solution for your Django
project, and to grasp its potential impact on your deployment process. For any questions or feedback, please open a `discussion <https://github.com/tobi-de/falco/discussions>`_.
