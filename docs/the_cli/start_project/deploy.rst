:description: How to deploy a project generated with falco.

Deployment
==========

.. warning::

    If this is your first time deploying a django project or you are a beginner, this is likely going to be confusing, I recommend checkout my  `Utilmate deployment guide for django <https://falco.oluwatobi.dev/guides/deployment.html>`_
    and follow the process described there, it's going to be more manuuall but you'l; get to learn more and you''l have an easier time degubgging any issues that arise.
    This guide is based on the same prinicples but is meant to automate a bunch of the process and might feel overwheling if you haven't aleardy dable around the land of deploying a  few times.

There are two options configured option to deploy project generated with falco, the first option is centered around the traditional vps stack deployment but with a lot of tools to automate the process, the second option
is centered around deploying using docker, this should also work with any PAAS service that support docker like caprover, coolify, digital ocean app platform, fly.io, heroku, render, etc.

Common Setup
------------

Let's first discuss the few common points between the two options.


Static files
************

In both cases staticfiles are serve by whitenoise, so there is not much for you to do here, static files are collected when the docker image is built, and bundle directly with the binary.

.. tip::

    All the commands related to building the app in anywa for production when possible are referenced in the ``justfile``, if you think something is missing, `let me know <https://github.com/tobi-de/falco/discussions>`_.

Media files
***********

By default media files are configured to be be stored using the filesystemd storage, so by default they will be saved at whatever location is defined by ``MEDIA_ROOT``
and the value of this settings is configurable via  environment variable with the same name.
`django-storages <https://github.com/jschneier/django-storages>`_ is also include  in the project, with the default configuration set to use `s3 <https://aws.amazon.com/s3/>`_.
This is what I personally use, to make use of this instead of the filesystem storage you need to set the environment variables below

.. tabs::

    .. tab:: Environment variables

        .. code-block:: bash
            :caption: Example

            USE_S3=True
            AWS_ACCESS_KEY_ID=your_access_key
            AWS_SECRET_ACCESS_KEY=your_secret_key
            AWS_STORAGE_BUCKET_NAME=your_bucket_name
            AWS_S3_REGION_NAME=your_region_name

    .. tab:: settings.py ( media root )

        .. literalinclude:: /_static/snippets/settings.py
            :linenos:
            :lineno-start: 168
            :lines: 168-168

    .. tab:: settings.py ( storage backend )

        .. literalinclude:: /_static/snippets/settings.py
            :linenos:
            :lineno-start: 229
            :lines: 229-246

This `guide <https://testdriven.io/blog/storing-django-static-and-media-files-on-amazon-s3/>`_ is an excellent resource to help you setup an s3 bucket for your media files.

.. important::

    If you are using docker and the filesystem storage make sure to add a volume to the container to persist the media files and
    If you are using caprover check out this `guide <https://gist.github.com/Tobi-De/7751c394570cbf0d7beb852304394046>`_ on how
    to serve the media files with nginx

Datababse
*********

There is no specific setup done for the database, you deal with this how you want. If you go with a managed solution like `aiven <https://aiven.io/postgresql>`_ they usually provide a backup solution,
it you also go with a PaaS to host your plateform fo your solution they usually provide a database service with automatic backup.

If you are using postgresql in production, a simple solution is to use `django-db-backup <https://github.com/jazzband/django-dbbackup>`_ with ``django-q2`` for the task that automatically backups, if you are using sqlite
I recommend `django-litestream <https://github.com/Tobi-De/django-litestream>`_.
I've being ridin myserlf the sqlite bandwagon recently and for my personal projects my go to has being ``sqlite + litestream``, I even have a branch for this on the `tailwind falco blueprint <ttps://github.com/Tobi-De/falco_tailwind/pull/67>`_.
This is evenetually going come to come to the default falco setup.


Cache
*****

The cache backend is configure to use `diskcache <https://github.com/grantjenks/python-diskcache>`_.

    DiskCache is an Apache2 licensed disk and file backed cache library, written in pure-Python, and compatible with Django.

    -- diskcache github page

By default it's not enable, all you have to do to enable it is to add the ``LOCATION`` environment variable with the path to the cache directory.

.. tabs::

    .. tab:: Environment variable

        .. code-block:: bash
            :caption: Example

            CACHE_LOCATION=.diskcache


    .. tab:: settings.py

        .. literalinclude:: /_static/snippets/settings.py
            :linenos:
            :lineno-start: 41
            :lines: 41-50


If you are running in docker, you can tadd a volume to the container to persist the cache files.

Sending Emails
**************

`django-anymail <https://anymail.dev/en/stable/>`_ is what is used by the project for emails sending, they support a lot of emails, provider, by default the project
is configured to use `ses <https://aws.amazon.com/ses/>`_. The same environmments variables

.. tabs::

    .. tab:: Email Backend

        .. literalinclude:: /_static/snippets/settings.py
            :linenos:
            :lineno-start: 71
            :lines: 71-75

    .. tab:: Anymail config

        .. literalinclude:: /_static/snippets/settings.py
            :linenos:
            :lineno-start: 351
            :lines: 351-359

It uses the environments variables so the same keys as for media files, this might be considered bad pratice by some, feel free to change them.

Environment Variables
*********************

These are te mininum required environment variables to make your project run:

.. code-block:: bash

    SECRET_KEY=your_secret_key
    ALLOWED_HOSTS=your_host
    DATABASE_URL=your_database_url
    ADMIN_URL=your_admin_url # not required but recommended


VPS Stack
---------

steps:

1 - Rename `someuser` to server user in ``deploy/etc/systemd/system/myjourney.service``
2

When you push the build binary file to a vps, you can use it as the example above shows if you move it to a folder on your path, just strip out the ``just run`` part.

.. code-block:: shell
   :caption: Example of pushing the binary to a vps

   curl -L -o /usr/local/bin/myjourney https://github.com/user/repo/releases/download/latest/myjourney-x86_64-linux
   chmod +x /usr/local/bin/myjourney
   myjourney # Run at least once with no argument so that it can install itself
   myjourney self metadata # will print project name and version

.. todo:: Reminder for self

    - merge this

Docker Based
------------

The dockerfile is located at ``deploy/Dockerfile`` and there is no ``compose.yml`` file. The setup is a bit unorthodox and use `s6-overlay <https://github.com/just-containers/s6-overlay>`_ to run everything needed for
the project in a single container.

.. admonition:: s6-overlay
    :class: note dropdown

    `s6 <https://skarnet.org/software/s6/overview.html>`_ is an `init <https://wiki.archlinux.org/title/Init>`_ system, think like `sytstemd <https://en.wikipedia.org/wiki/Systemd>`_ and
    ``s6-overlay`` is a set of tools and utilities to make it easier to run ``s6`` in a container environnment. A common linux tool peope often use in the django eocsytem that could serve as a replacement for example is `supervisord <http://supervisord.org/>`_.
    The ``deploy/etc/s6-overlay`` file contains the all the ``s6`` configuration, it will be copied in the the container in the ``/etc/s6-overlay`` directory. When the containers starts it will run a one-shot script (in the ``s6-overlay/scrips`` folder)
    that will run the setup function in the ``__main__.py`` file, then two lon process wil be run, one for the gunicorn server and one for the django-q2 worker.



There is the github action file at ``.github/workflows/cd.yml`` that will do the actual deployment. This action is run everytime a new `git tag is pushed to the repository </the_cli/start_project/packages.html#project-versioning>`_.

CapRover
********

Assuming you already have a caprover instance setup, all you have to do here is update you gihub repository with the correct credentials.
Here is an example of the content of the ``deploy-to-caprover`` job.

.. literalinclude:: /_static/snippets/cd.yml
    :lines: 9-21
    :language: yaml

Checkout the the `action readme <https://github.com/adamghill/build-docker-and-deploy-to-caprover>`_ for more informations, but there is essentially two things to do, add two secrets to your github repository:

``CAPROVER_SERVER_URL``: The url of your caprover server, for example ``https://caprover.example.com``
``CAPROVER_APP_TOKEN``: This can be generated on the ``deployment`` page of your caprover app, there should be an ``Enable App Token`` button.

If you are deploying from a private repository, the is also `instructions <https://github.com/adamghill/build-docker-and-deploy-to-caprover?tab=readme-ov-file#unauthorized-error-message-on-caprover>`_ to allow caprover to pull from your private repository.

And tha't basically it, if you are a caprover user, you know the rest of the drill.

Other PAAS
**********

If you using a PAAS solution that support docker, the first thing you need to do is update the ``.github/workflows/cd.yml`` action file to build your image and push it to a registry.
If you want the  `github registry <https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry>`_ your new job might look something like
this using `this action <https://github.com/docker/build-push-action>`_:

.. code-block:: yaml

  build-and-push-image:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - name: Docker meta
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/username/projectname # CHANGE THIS
          # generate Docker tags based on the following events/attributes
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=semver,pattern={{major}}
            type=sha

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.repository_owner }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Checkout Code Repository
        uses: actions/checkout@v4

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          push: true
          context: .
          file: deploy/Dockerfile
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max




I put up the action above based on these examples, yo can look them up to adjust the action to your needs:

- https://docs.docker.com/build/ci/github-actions/push-multi-registries/
- https://docs.docker.com/build/ci/github-actions/manage-tags-labels/

.. note::

    You can also build the image locally with ``just build-docker-image`` and then push it manually on the registry of your choice.


At this point the process will be plateform dependent, but usually you should be abloe to specify the Image to pull from and that's should be it.
Eventually in the future I might add more specific guides for some of the most popular PAAS solutions.
