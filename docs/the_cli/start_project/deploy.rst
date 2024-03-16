:image: https://raw.githubusercontent.com/Tobi-De/falco/main/assets/og-image.jpg
:description: How to deploy a project generated with falco.

Deployment
==========

The generated projects comes with a configuration for a docker based deployment. The container use s6-overlay to run both the django main server using
using and a worker process for qcluster. If've you read a bit behind the philosophy behind the s6-overlay project, the idea is to having everything  necesseray
to run your project in a single container, your database, maybe the database, redis, etc. The default setup is quite simple, so if you an onboard with the idea
you can add more services to the setup and if not you can just limit it to django and django-q2 and having everything else deployed externally.

.. note::

    For more details on s6-overlay, read the guide `on it </guides/running_project_in_a_container.html>`_.


**The basics**

- The staticfiles are served with whitnoises, there is almost nothing to do on your side for this work in production, the files are collected when the docker image is build
- There is no special configuration for the mediafiles, they will be stored directly on disk (in the container) if this is not changed, if your app really need them is it recommand to use something like django-storages to host and serve them from an object storage (AWS S3, minio, cloudinary, etc.)
- The wsgi use to run the django project is gunicorn with a custom config file meant to make the most of your cpu cores
- There is no configuations regarding a reverse proxy like nginx
- There no configuration included to deal with domain names and certificiates obtentions

The dockefile define a healh check ur, you can check it with

.. code-block:: shell

    docker inspect --format "{{ json .State.Health }}"


I mostly deploy my project using caprover, so this guide will mainly focus on the deployment process using caprover with some reference for non caprover users.

.. note::

    If you never deployed an app before, readd the `deployment guide </guides/deployment.html>`_ it should give you an overview of everything you need to knwon


Common ground
-------------

- The staticfiles are configured to used 


Non Caprover users
------------------

Let's get this out the way first, this is what you need to known.

The dockerfile that comes with the project with build you project and collectsatic staticfiles, staticfiles are served with whitenoise, so there should be no additional
setup needed to make if work.
Everything is already taking care on the django side, what you'll need now is a reverse proxy so stand in front of gunicorn. The most common choice is 



Caprover
--------

Auto deployment from Github
***************************

Webhook
+++++++

Github Action
+++++++++++++


Media files
***********


Databases
*********


Extra
-----

- uptime monitoring service, eg uptime kuma (healthcheck)
- log aggregation service
- sentry
- log aggregation services, signoz




.. The ``deploy`` folder contains some files that are needed for deployment, mainly docker related. If Docker isn't part of your deployment plan, this directory can be safely removed.
.. However, you might want to retain the ``gunicorn.conf.py`` file inside that directory, which is a basic Gunicorn configuration file that could be useful regardless of your chosen deployment strategy.

.. The project comes for docker and s6-overlay configuration for deployment. All deployment related files are in the ``deploy``folder.
.. s6-overay is an init service, uses for processes supervisation meant for
.. container. It is build around the s6 system. For more details on how s6-overlay check the dedicated guide on it.
.. All you need to known is  that the container produced by the image, is meant to run your django project using gunicorn and django-q2 for background tasks
.. and scheduling feature. For more details on django-q2 checkout the guides on task quues and schedulers in django.
