:description: Offload tasks in django using task queues and periodic tasks using schedulers.

Task Queues and Schedulers
==========================

Task queues are used to offload tasks to a dedicated worker process when the processing of those tasks does not fit into a traditional request-response cycle.
Basically, if you need to do something that might take too long to process and whose result does not need to be shown immediately to the user, you use a queue manager.
Think of them like virtual to-do lists for your web application. When a task is too time-consuming to be handled immediately, it gets added to the queue.
A dedicated worker process then picks up tasks from the queue and processes them in the background, freeing up your web application to handle other requests quickly.

.. admonition:: Example

        Imagine...


Schedulers are used to periodically run tasks. Essentially, they help you schedule tasks to be run at specific times and/or intervals. Imagine you need to send an email to your users
every day at 8:00 AM; you can use a scheduler to do that.

There are many options available in the `django third-party ecosystem <https://djangopackages.org/grids/g/workers-queues-tasks/>`__, some focus solely on providing a task queue,
others are just schedulers and many of them provide both in one package. You can also search for purely python solutions and
integrate them into your django project yourself.

I prefer options that do not require additional infrastructure (redis, rabbitmq, etc.) for simple tasks.
For more complex tasks, I tend to choose a solution that supports redis as a task broker.

.. hint::
    :class: dropdown

    A broker in this context is a service that is used to store the tasks that need to be processed. The most
    common ones are `redis <https://redis.io/>`__ and `rabbitmq <https://www.rabbitmq.com/>`__.

.. note::
   My current pick in this list is **django-q2**. It is a fork of the original **django-q** project, which is no longer maintained.

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
| django-dramatiq   | https://github.com/Bogdanp/django_dramatiq         | Yes        | No         | Yes                         |
+-------------------+----------------------------------------------------+------------+------------+-----------------------------+
| django-rq         | https://github.com/rq/django-rq                    |            |            |                             |
|                   |                                                    | Yes        | Yes        | Yes                         |
|                   | https://github.com/dsoftwareinc/django-rq-scheduler|            |            |                             |
+-------------------+----------------------------------------------------+------------+------------+-----------------------------+
| procrastinate     | https://github.com/procrastinate-org/procrastinate | Yes        | Yes        | No                          |
+-------------------+----------------------------------------------------+------------+------------+-----------------------------+
| django-chard      | https://github.com/drpancake/chard                 | Yes        | No         | No                          |
+-------------------+----------------------------------------------------+------------+------------+-----------------------------+
| celery            | https://github.com/celery/celery                   | Yes        | Yes        | Yes                         |
+-------------------+----------------------------------------------------+------------+------------+-----------------------------+

.. admonition:: Auto reload in development
    :class: dropdown

    If you are using one of these you might want an automatic reload feature when files changes in dev, you can use the ``hupper``
    python package for that purpose. It watches for file changes in the cruurent directory and restarts the worker process automatically.

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


Deploying with a task queue
---------------------------
