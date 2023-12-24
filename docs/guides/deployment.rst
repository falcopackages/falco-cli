:description: Smooth Deployment Strategies for django projects

Deploy your project
===================


Intro

Static Files
------------

Media Files
-----------

Media files in django usually refer to files uploaded by users, profile pictures, product images, etc.
I usually manage my media files using `django-storages <https://github.com/jschneier/django-storages>`__.
Here is how I set it up.

.. code:: python

   # core/storages.py
   from storages.backends.s3boto3 import S3Boto3Storage

   class MediaRootS3Boto3Storage(S3Boto3Storage):
       location = "media"
       file_overwrite = False


   # settings.py - production settings
   AWS_ACCESS_KEY_ID = env("DJANGO_AWS_ACCESS_KEY_ID")
   AWS_SECRET_ACCESS_KEY = env("DJANGO_AWS_SECRET_ACCESS_KEY")
   AWS_STORAGE_BUCKET_NAME = env("DJANGO_AWS_STORAGE_BUCKET_NAME")
   DEFAULT_FILE_STORAGE = "project_name.core.storages.MediaRootS3Boto3Storage"
   MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/"


Database
--------

WSGI server
-----------

**Process Managers**

Web server
----------

https://www.nginx.com/
https://www.nginx.com/products/nginx-unit/
https://httpd.apache.org/
https://caddyserver.com/

Resources
---------

Django Deployment Checklist
https://youtu.be/t-wsiW5mkgA?si=WsXQIuO4kDwGKrVO
https://github.com/ehmatthes/django-simple-deploy
https://github.com/lincolnloop/django-production



Deployment Platforms
--------------------

Deployment is not a solved solution for me, it is still a pain, no matter how many time I do it, it never goes smoothly. If you can afford it I'll recommend
a managed solution (the cloud), if for any reason you decide to go the self-hosting route, I'll recommend you use a P.A.A.S (Platform as a Service) solution
to ease your burden or a least docker as a bare minimum.

.. Deployment is not worth your blood and energy my friend.

Paas and rent a VPS


Managed solutions
^^^^^^^^^^^^^^^^^

I don't have much experience with these, but are relatively similarly price and quite easy to use, so you can just use one.

* `Fly <https://fly.io/>`_
* `Render <https://render.com/>`_
* `AWS Elastic Beanstalk <https://aws.amazon.com/elasticbeanstalk/>`_
* `Heroku <https://www.heroku.com/>`_
* `Railway <https://railway.app/>`_
* `Appliku <https://appliku.com>`_


Self-Managed solutions
^^^^^^^^^^^^^^^^^^^^^^

If you are new to it, the term **self-hosting** might be misguidind, usually people use self-hosting to just mean you rent a vps and to the work yourself
instead of paying someone else to do it for you. It might be cheaper but if you want to do real **self-hosting** you technically need to by you own hardware.
But I digress, the point of this section is to present you tools that will easier your burden if you decide de rent a server instead of using a managed solution.
I find that self-hosted solutions are generally cheaper than managed/hosted solutions, but I don’t have much experience with managed solutions,
so I could be wrong, do your own research and if you can afford it, try them out to see what works best for you.


P.A.A.S (Platform as a Service)
*******************************

.. hint::

   My personal favorite is `caprover <https://caprover.com/>`_


**CapRover**

   "CapRover is an extremely easy to use app/database deployment & web server manager for your NodeJS, Python, PHP, ASP.NET, Ruby, MySQL, MongoDB, Postgres, WordPress (and etc…) applications!"

   -- `CapRover Official Site <https://caprover.com/>`_


CapRover is a self-hosted `PaaS <https://en.wikipedia.org/wiki/Platform_as_a_service>`__ solution, think `heroku <https://www.heroku.com/>`__ but on your own servers.
Nowadays, I tend to prefer PaaS solutions over manual deployment and configuration, as they are easy to use with little configuration to deploy most apps.
Software is usually quite a pain to deploy and even though I’ve gotten better at it over time, I’ll always choose a managed solution over manual deployment.

After installing CaProver with the `getting started guide <https://caprover.com/docs/get-started.html>`__, there is not much left to do, create a new application and in the section ``deployment``.
configure your application using the third method ``Method 3: Deploy from Github/Bitbucket/Gitlab``.

.. tip::

   If you use github, instead of entering your password directly into the ``password`` field, you can use a `personal access token <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token>`__,
   which is a more secure option.

.. note::

   Checkout `caprover automatic deploy <https://caprover.com/docs/deployment-methods.html#automatic-deploy-using-github-bitbucket-and-etc>`__ to automate the deployment of your applications.


If you have generate a template with the ``falco`` cli or you have a dockerfile at your disposal, the only config you need in your projec to run caprover is this

.. code-block:: text
   :caption: captain-definition

   {
      "schemaVersion": 2,
      "dockerfilePath": "./docker/Dockerfile" # the path to your dockerfile
   }

-  `Dokku <https://dokku.com/>`_
-  `Coolify <https://github.com/coollabsio/coolify>`_
-  `DigitalOcean App Platform <https://www.digitalocean.com/products/app-platform>`_


Bare-bone VPS
*************

.. hint::

   My personal pick is Linode

* `Linode <https://www.linode.com/>`_
* `DigitalOcean <https://www.digitalocean.com/>`_
* `Vultr <https://www.vultr.com/>`_
* `PythonAnywhere <https://www.pythonanywhere.com/>`_


I recently discovered `django-simple-deploy <https://github.com/ehmatthes/django-simple-deploy>`__ which can configure your django project.
