:image: https://raw.githubusercontent.com/Tobi-De/falco/main/assets/og-image.jpg
:description: Deployment concepts, plateforms and strategies for django projects.

The ultimate deployment guide
=============================

This guide dives into the fundamentals of deployment, covering concepts that are common to all deployment processes. Regardless of the process or strategies you choose, this knowledge will be beneficial.
Alongside this, the guide also provides a list of various deployment platforms and strategies, coupled with some personal recommendations. The `original version <https://tobi-de.github.io/fuzzy-couscous/deployment/>`_ of this guide
was merely a list of platforms. However, after watching the DjangoCon 2023 talk, `What Django Deployment is really About by James Walters <https://www.youtube.com/watch?v=t-wsiW5mkgA>`_, I felt inspired
to write something more useful.

Since concrete examples often speak louder than words, each section (where applicable) includes a set of instructions on how to deploy a Django-based personal journal app named **myjourney** on a virtual
private server running Ubuntu 22.04. My go-to for this setup is this `DigitalOcean guide <https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-22-04>`_.
It's an excellent resource that I find myself returning to whenever my memory fails to cooperate!

These notes, which are hidden by default (you'll find one right below), can serve either as a step-by-step guide or a handy reference for future use.

.. admonition:: deploying myjourney - prerequisites
   :class: note dropdown

   - A budget-friendly virtual private server (VPS), keep reading for some suggestions.
   - An affordable domain name, consider some inexpensive top-level domains (TLD) like .xyz, .online, .site, etc.

   If you are a student, you can also get a plethora of free resources with the `github student pack <https://education.github.com/pack>`_.

   1. Clone the repository on the server

      .. code-block:: bash
         :caption: Clone the repository

         git clone https://github.com/tobi-de/myjourney.git

   2. Install dependencies

      .. code-block:: bash
         :caption: Install python dependencies

         sudo apt install python3-pip python3-venv python3-dev python-is-python3 libpq-dev

   3. Create a virtualenv and install requirements

      .. code-block:: bash
         :caption: Create a virtual environment

         cd myjourney
         python -m venv venv
         source venv/bin/activate
         python -m pip install -r requirements.txt


Web server
----------

The primary roles of a web server are to deliver static files and function as a `reverse proxy <https://en.wikipedia.org/wiki/Reverse_proxy>`_ for the application server, also known as the WSGI server.
When a user sends a request to your website, the web server is the initial component to process it. The web server receives the request, forwards it to the WSGI server (which operates your Django application),
collects the response from the application, and then delivers it back to the client (the user's web browser).
Moreover, the web server, when properly configured, can intercept requests for static files (HTML, CSS, JavaScript, images, etc.) and serve them before they reach the application server. This is because many
application servers are either not designed to handle such requests or do so inefficiently.
In a production environment, your Django application will likely operate behind a web server, serving as its translator or guide to the broader world of the internet.

The most popular web servers are `nginx <https://www.nginx.com/>`_ and `apache <https://httpd.apache.org/>`_, with **nginx** being the one you'll encounter most frequently these days.

Nginx is a reliable and well-established solution that has powered and still powers countless websites. It should serve your needs adequately. However, if you're interested in exploring new alternatives, here are two projects that are worth checking out:

- `nginx-unit <https://www.nginx.com/products/nginx-unit/>`_: A universal web app server that combines several layers of the typical application stack into a single component.
- `caddy <https://caddyserver.com/>`_: Caddy offers automatic TLS certificate obtainment and renewal, HTTP/2, flexible configuration, better security defaults, observability, and more.

.. admonition:: deploying myjourney - nginx
   :class: note dropdown

   1. Install nginx

   .. code-block:: bash
      :caption: Install nginx

      sudo apt install nginx

   2. Create an nginx configuration file for your project

   .. code-block:: bash
      :caption: Configure nginx

      sudo touch /etc/nginx/sites-available/myjourney

   1. Update the file with the following content

   .. code-block:: text
      :caption: /etc/nginx/sites-available/myjourney

      server {
         listen 80;
         server_name myjourney.com YOUR.SERVER.IP.ADDRESS;

         location / {
            proxy_pass http://unix:/run/gunicorn.sock;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
         }
      }


**Reverse proxies**

If you don't require the static file serving capabilities of web servers and are interested in a more modern approach, you might consider using specialized reverse proxies.
Reverse proxies primarily handle the routing of requests to the WSGI server. While Nginix has this capability and is often used as a reverse proxy, pure reverse proxy solutions
may offer features that Nginix does not. One such popular solution is `traefik <https://traefik.io/traefik/>`_, known for features like automatic SSL certificate generation,
automatic routing, blue-green deployment, etc. It is also considered simpler to set up.

.. todo::

   Add an example of traefik config

WSGI server
-----------

The WSGI server, also known as the **application server**, is responsible for running your Django application. This server is needed because some web servers, like nginx, are not capable of
executing Python code directly. `Gunicorn <https://gunicorn.org/>`_, a popular WSGI server for Django, fulfills this role.

Gunicorn can be configured using a Python file, such as `this one <https://github.com/Tobi-De/falco_blueprint_basic/blob/main/%7B%7B%20cookiecutter.project_name%20%7D%7D/deploy/gunicorn.conf.py>`_ provided with a generated Falco project.
However, its most basic usage is:

.. code-block:: bash
   :caption: Run gunicorn

   gunicorn myproject.wsgi:application

In this command, Gunicorn needs your Django application as its first argument. For most Django projects, this is specified in the ``wsgi.py`` file which contains a variable named ``application``. ``myproject`` refers to the
directory where the ``wsgi.py`` file is located. For projects created with Falco, the ``wsgi.py`` file is typically located in the ``config`` directory. Therefore, the command would be:

.. code-block:: bash
   :caption: Run gunicorn

   gunicorn config.wsgi:application

So, what is this **WSGI** we've been talking about?

    "WSGI, or Web Server Gateway Interface, is a specification that describes how a web server communicates with web applications, and how web applications can be chained together to process one request."

    -- `WSGI official docs <https://wsgi.readthedocs.io/en/latest/what.html>`_

Gunicorn is just one of many available application servers. Other servers like `hypercorn <https://pgjones.gitlab.io/hypercorn/>`_ and `granian <https://github.com/emmett-framework/granian>`_ offer similar functionality, each with
their own unique features. Regardless of the server used, they all require a way to know how to run your Django application. That's where ``WSGI`` comes in. WSGI provides a universal specification for writing Python web applications
that can be run by any server adhering to the standard, independent of specific web server implementation details.

   **WSGI** serves as a common language that Python web servers (such as Gunicorn) use to communicate with Python web applications (like Django).

.. admonition:: What about ASGI?
   :class: note dropdown

   WSGI is not the only standard for Python web servers. `ASGI <https://asgi.readthedocs.io/en/latest/>`_, designed for async-capable servers, is another option. However, when it comes to Django, I don't really care about ASGI (at least for now), but that's just me :)

**Process Managers**

Hosting a project on your own server requires more than just an application server. You also need a **process manager**. This manager starts and stops your application server and restarts it if it crashes. For instance, if you SSH into your server and run the **gunicorn** command, your app
will work and, assuming nginx is configured correctly, you'll even be able to access it via your IP address or domain name. However, if you close your SSH session, your app will stop functioning. This is where the process manager comes in. It runs your app in the background, ensuring
it is always running, even if your server restarts.

The two most widely used process managers are `supervisor <http://supervisord.org/>`_ and `systemd <https://systemd.io/>`_. Systemd is typically built-in to most Linux distributions, while Supervisor requires manual installation. Despite this, both process managers serve the same purpose effectively.
From my experience, there's no significant difference in their user experience.

.. admonition:: deploying myjourney - gunicorn with systemd
   :class: note dropdown

   1. Create a systemd service file for your project

   .. code-block:: bash
      :caption: Configure systemd

      sudo touch /etc/systemd/system/gunicorn.service

   1. Replace the file's content with the following code, sourced from https://docs.gunicorn.org/en/stable/deploy.html#systemd

   .. code-block:: text
      :caption: /etc/systemd/system/gunicorn.service

      [Unit]
      Description=gunicorn daemon
      Requires=gunicorn.socket
      After=network.target

      [Service]
      User=user
      Group=www-data
      WorkingDirectory=/home/user/myjourney
      EnvironmentFile=/home/user/myjourney/.env
      ExecStart=/home/user/myjourney/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock config.wsgi:application
      ExecReload=/bin/kill -s HUP $MAINPID
      KillMode=mixed
      TimeoutStopSec=5
      PrivateTmp=true

      [Install]
      WantedBy=multi-user.target

   A comprehensive explanation of all gunicorn options can be found `here <https://docs.gunicorn.org/en/stable/run.html#commonly-used-arguments>`_.
   Remember, the value assigned to the ``--bind`` option should match the one specified in the nginx config file, specifically on the ``proxy_pass`` line.
   Nginx and gunicorn communicate with each other using this `sock file <https://fileinfo.com/extension/sock>`_. Though it's possible to replace it with an IP address and port number (e.g., 127.0.0.1:8000),
   using the sock file is generally more efficient as it is a more direct connection.

   1. Start the gunicorn service

   .. code-block:: bash
      :caption: Start gunicorn

      sudo systemctl start gunicorn

   To access the log of your application you can use the command below:

   .. code-block:: bash
      :caption: Access gunicorn logs

      sudo journalctl -e -u gunicorn.service

   To check the status of your application you can use the command below:

   .. code-block:: bash
      :caption: Check gunicorn status

      sudo systemctl status gunicorn



Static Files
------------

Static files are your HTML, CSS, JS, images, and so forth. As the name suggests, these **static** files come bundled with your application.

Below are the main Django settings related to static file management for deployment:

.. code-block:: python
   :caption: settings.py

   STATIC_URL = '/static/'
   STATIC_ROOT = BASE_DIR / 'staticfiles'

The ``STATIC_URL`` is the URL to use when referring to static files located in ``STATIC_ROOT``. Given the settings above, if a file named ``style.css``
is located in ``BASE_DIR / 'staticfiles'``, you can access it at ``/static/style.css``.

During development, serving static files is handled by the development server. However, in a production environment, this is typically the role of a web server.
For example, you might configure Nginx to serve all requests coming to ``/static/`` from the ``staticfiles`` directory.

For more sophisticated options to manage your static files, consider the following:

- Serving your static files using `whitenoise <https://whitenoise.readthedocs.io/en/latest/>`_
- Using `whitenoise behind a CDN <https://whitenoise.readthedocs.io/en/latest/django.html#use-a-content-delivery-network>`_ for your static files
- Storing and serving the files on `AWS S3 with django-storages <https://testdriven.io/blog/storing-django-static-and-media-files-on-amazon-s3/>`_


.. admonition:: deploying myjourney - static files
   :class: note dropdown

   1. Run the collectstatic command to put your static files in the ``STATIC_ROOT`` directory

   .. code-block:: bash
      :caption: Collect static files

      cd myjourney
      python manage.py collectstatic

   2. Update the nginx config file with the following content

   .. code-block:: text
      :caption: /etc/nginx/sites-available/myjourney
      :linenos:
      :emphasize-lines: 5-7

      server {
         listen 80;
         server_name myjourney.com YOUR.SERVER.IP.ADDRESS;

         location /static/ {
            alias /home/user/myjourney/staticfiles/;
         }

         location / {
            proxy_pass http://unix:/run/gunicorn.sock;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
         }
      }



Media files
-----------

Django's media files usually refer to user-uploaded files, such as profile pictures, product images, and so forth. While serving these files with Django is not ideal, it differs from static
files as there are no well-maintained projects (like Whitenoise) available to serve media files. Therefore, this task is typically handled by an external service.

There are various ways to serve media files. The simplest method is to let Nginx (or your chosen web server) serve them. However, safer and often better solutions include using `object storage solutions <https://aws.amazon.com/what-is/object-storage/>`_
such as `AWS S3 <https://aws.amazon.com/s3/>`_, `DigitalOcean Spaces <https://www.digitalocean.com/products/spaces/>`_, and `Google Cloud Storage <https://cloud.google.com/storage>`_, among others.
You can use a package like `django-storages <https://django-storages.readthedocs.io/en/latest/>`_ to help you upload your media files to these services.
The advantage of using an **object storage solution** is the ability to have fine-grained access control over your media files.

The following django settings deal with media file management:

.. code-block:: python
   :caption: settings.py

   MEDIA_URL = '/media/'
   MEDIA_ROOT = BASE_DIR / 'media'

The ``MEDIA_URL`` is the URL used to serve media from ``MEDIA_ROOT``. This follows the same logic as with static files. For instance, if a file named ``profile.jpg`` is located in ``BASE_DIR / 'media'``, you can access it at ``/media/profile.jpg``.

Here's an insightful video on `serving media files from S3 + Cloudfront <https://youtu.be/RsiXzwesNLQ?si=jBpVvIcYjhopTVt7>`_ if you want to try the object-storage approach.

.. admonition:: deploying myjourney - media files
   :class: note dropdown

   Update the nginx config file with the following content

   .. code-block:: text
      :caption: /etc/nginx/sites-available/myjourney
      :linenos:
      :emphasize-lines: 9-11

      server {
         listen 80;
         server_name myjourney.com YOUR.SERVER.IP.ADDRESS;

         location /static/ {
            alias /home/user/myjourney/staticfiles/;
         }

         location /media/ {
            alias /home/user/myjourney/media/;
         }

         location / {
            proxy_pass http://unix:/run/gunicorn.sock;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
         }
      }


Database
--------

The database is where your data resides. Django offers support for a wide range of databases, both through `official <https://docs.djangoproject.com/en/5.0/ref/databases/>`_ and `third party <https://djangopackages.org/grids/g/database-backends/>`_ backends.
A Django database backend serves as a bridge that allows Django to access the unique features of a specific database through a consistent interface. It takes care of the intricate details specific to the implementation of its targeted database.

   The most popular database choice for Django is `Postgres <https://www.postgresql.org/>`_.

Setting up a proper database infrastructure involves many aspects such as automatic backup, maintenance, security, and more, which can be quite challenging to get right.
If, like me, you're not an expert on the subject, I would suggest using a Database as a Service (DBaaS) for any serious production project.
These are managed database services that delegate the complex task of managing and maintaining your database to experts.

The official PostgreSQL site has a section on `DBaaS providers for PostgreSQL <https://www.postgresql.org/support/professional_hosting/>`_, which could be a good starting point.

The configuration on Django's end is relatively simple, the example below showcase the settings for a PostgreSQL database.

.. code-block:: Python
   :caption: settings.py

   DATABASES = {
      "ENGINE: "django.db.backends.postgresql",
      "NAME": env("DATABASE_NAME"),
      "USER": env("DATABASE_USER"),
      "PASSWORD": env("DATABASE_PASSWORD"),
      "HOST": env("DATABASE_HOST"),
      "PORT": env("DATABASE_PORT"),
   }

You could use packages such as `django-environ <https://django-environ.readthedocs.io/en/latest/api.html#environ.Env.db>`_ or `dj-database-url <https://github.com/jazzband/dj-database-url/>`_ to simplify the settings configuration into a single line, which would then be dependent on a single environment variable (e.g. ``DATABASE_URL``).


.. admonition:: deploying myjourney - postgres setup
   :class: note dropdown

   1. Install postgres

   .. code-block:: bash
      :caption: Install postgres

      sudo apt install postgresql postgresql-contrib

   1. Create a database for your project

   .. code-block:: bash
      :caption: Create database

      sudo -u postgres createdb myjourney

   1. Create a user for your project

   .. code-block:: bash
      :caption: Create user

      sudo -u postgres psql
      postgres=# CREATE USER myjourneyuser WITH PASSWORD 'password';
      postgres=# ALTER ROLE myjourneyuser SET client_encoding TO 'utf8';
      postgres=# ALTER ROLE myjourneyuser SET default_transaction_isolation TO 'read committed';
      postgres=# ALTER ROLE myjourneyuser SET timezone TO 'UTC';
      postgres=# GRANT ALL PRIVILEGES ON DATABASE myjourney TO myjourneyuser;



Summary
-------

.. container:: image-2

   .. image:: ../images/deployment.png


If there is one key takeaway from this guide, it's the diagram above. It illustrates the essential components of any deployment process:

1. The client makes a request to the web server.
2. The web server passes the request to the WSGI server.
3. The WSGI server runs your Django application and builds a response using the database.
4. The WSGI server sends the response back to the web server.
5. The web server sends the response back to the client.

This process is universal and remains essentially unchanged across various implementations. Even though the components may vary, or some platforms may obscure certain elements, or
even if components are duplicated (perhaps to handle more load) or new components are introduced, the basics are almost always present in some form.


Platforms
---------

Now, let's discuss deployment platforms, which are where you actually host your application. Despite everything mentioned above, you are likely to run into some minor issues.
The essential concepts remain the same, but not all platforms are built equally. Some might make the work easier for you than others.

If you can afford it, I recommend a managed solution (the cloud). The next best alternative is a self-hostable P.A.A.S (Platform as a Service) solution on your own server to ease your burden,
or at the very least, Docker as a bare minimum. The goal is to find a workflow that minimizes manual configuration and works best for you.

There are solutions like `Ansible <https://www.ansible.com>`_ that can help automate the deployment process, but Docker seems to be the most popular and one of the simplest solutions these days.
With that said, the less work you have to do on your own, the more it usually costs. Below, I'll go over some solutions
I can recommend, some of which even offer some kind of free usage to reduce your costs as much as possible.

.. admonition:: Disclaimer
   :class: important

   These are personal recommendations. There are no affiliated links or sponsorships unless explicitly stated otherwise :)


Managed solutions
^^^^^^^^^^^^^^^^^

These are the platforms that handle much of the infrastructure for you, in exchange for a higher cost. Typically, these require the least amount of work once you become familiar with how they work.
Even though my experience with these platforms is limited, they are generally similarly priced and quite user-friendly. The descriptions provided below are directly sourced from their respective websites.

* `DigitalOcean App Platform <https://www.digitalocean.com/products/app-platform>`_ : Build, deploy, and scale apps quickly using a simple, fully-managed infrastructure solution.
* `Fly <https://fly.io/>`_ : Fly.io transforms containers into micro-VMs that run on our hardware in 30+ regions on six continents.
* `Render <https://render.com/>`_ : Build, deploy, and scale your apps with unparalleled ease – from your first user to your billionth.
* `AWS Elastic Beanstalk <https://aws.amazon.com/elasticbeanstalk/>`_ : Deploy and scale web applications
* `Heroku <https://www.heroku.com/>`_ : Build data-driven apps with fully managed data services.
* `Railway <https://railway.app/>`_ : Railway is the cloud for building, shipping, and monitoring applications. No Platform Engineer required.

.. hint::

    A special mention goes to `Appliku <https://appliku.com>`_. While it does not provide direct hosting services,
    it offers an intuitive interface that simplifies deployment on various platforms such as AWS, Digital Ocean, and more.



Self-Managed solutions
^^^^^^^^^^^^^^^^^^^^^^

If you're new to the concept, the term **self-hosting** might be misleading. Typically, **self-hosting** is used to refer to the practice of renting a Virtual Private Server (VPS)
and handling all the work yourself, rather than paying someone else to do it for you. While this method might be cheaper, true **self-hosting** technically requires owning your
own hardware. From my experience, self-hosted solutions are generally less expensive than managed/hosted solutions. However, my experience with managed solutions is limited, so I
encourage you to do your own research. If your budget allows, consider trying both managed and self-managed solutions to see what works best for you.


Self-hostable P.A.A.S
*********************

These P.A.A.S solutions necessitate the purchase of your own server (unless you utilize their offerings), but they simplify your tasks by providing an experience akin to that of a managed solution.


**CapRover** - The choosen one :)

   "CapRover is an extremely easy to use app/database deployment & web server manager for your NodeJS, Python, PHP, ASP.NET, Ruby, MySQL, MongoDB, Postgres, WordPress (and etc…) applications!"

   -- `CapRover Official Site <https://caprover.com/>`_

In case it wasn't clear, caprover is my PaaS of choice.

-  `Dokku <https://dokku.com/>`_ : An open source PAAS alternative to Heroku.
-  `Coolify <https://github.com/coollabsio/coolify>`_ : An open-source & self-hostable Heroku / Netlify / Vercel alternative.


Bare-bone VPS
*************

This section introduces bare-metal solutions: a list of Virtual Private Servers (VPS) providers. This is likely the most affordable option, but it also requires the most effort on your part.
The offerings in this category are diverse in range and price, so you have plenty of choices. However, be prepared to invest more time unless you opt to automate some processes,
for instance, by using a tool like `ansible <https://www.ansible.com>`_.

.. admonition:: deploying myjourney - vps
   :class: note dropdown

   This is the option assumed in the guide for deploying myjourney.

* `Linode <https://www.linode.com/lp/refer/?r=c12ad16f52b3939fe11e3cee8e1ecaf2947125ab>`_ (referral link with 60 days of $100 credits)
* `DigitalOcean <https://m.do.co/c/507efee95715>`_ (referral link with 60 days of $200 credits)
* `Vultr <https://www.vultr.com/>`_
* `PythonAnywhere <https://www.pythonanywhere.com/>`_
* `Contabo <https://contabo.com/>`_

Personal Recommendations
^^^^^^^^^^^^^^^^^^^^^^^^

If you're feeling a bit overwhelmed by the options provided above, here are my personal recommendations:

If you're trying to learn and have never deployed a Django app before, try the full manual process a few times (2-3 times should do it). 
Once you get the hang of the process, buy a cheap VPS and install `caprover <https://caprover.com>`_. Try to stick with this setup for as 
long as you can, or as long as it is **enough**.

The day may come when this setup is no longer sufficient. You'll know it when it happens - you'll have thousands of users, tens of thousands of concurrent requests, 
and you'll want to offload most of the infrastructure management and maintenance to a managed service so you can focus on improving the core business logic.
When that day comes, you can opt for one of the managed solutions mentioned above (e.g., AWS, or AppLiku on top of AWS to ease the burden).
Personally, I've never reached that level of traffic, so I'm still managing all of my projects on a cheap `contabo VPS <https://contabo.com>`_ with `caprover <https://caprover.com>`_.

Resources
---------

- `myjourney github repository <https://github.com/Tobi-De/myjourney>`_: The source code for myjourney + some more deployment ressources.
- `Django Deployment Checklist <https://docs.djangoproject.com/en/dev/howto/deployment/checklist/>`_ : The official django deployment checklist.
- `django-simple-deploy <https://github.com/ehmatthes/django-simple-deploy>`_ : A reusable Django app that configures your project for deployment
- `django-up <https://github.com/sesh/django-up>`_ : django-up is a tool to quickly deploy your Django application to a Ubuntu 22.04 server with almost zero configuration.
- `django-production <https://github.com/lincolnloop/django-production>`_ : Opinionated one-size-fits-most defaults for running Django to production (or any other deployed environment).
- `ansible-django-stack  <https://github.com/jcalazan/ansible-django-stack>`_: Ansible Playbook for setting up a Django production server with Nginx, Gunicorn, PostgreSQL, Celery, RabbitMQ, Supervisor, Virtualenv, and Memcached.
- `django-flyio <https://github.com/avencera/rustywind?tab=readme-ov-file>`_: A set of simple utilities for Django apps running on Fly.io.


Alternative strategies
----------------------

The web is not the only medium to distribute your app. It's the most popular one, but certainly not the sole option.

Serverless
^^^^^^^^^^

The serverless trend appears to have slowed down lately, but there are still use cases. I have almost no experience with this approach, but it promises to run
your app without constantly active servers at the lowest possible cost.

Here's my understanding of the concept: most of the time, there is no server running your app. However, when a request comes in, a server is started, your app is run,
and then the server is stopped. A server is still involved, but it is not running all the time.

The most popular solution in the Python ecosystem seems to be `zappa <https://github.com/zappa/Zappa>`_.

Desktop / Mobile app
^^^^^^^^^^^^^^^^^^^^

Packaging your apps as mobile or desktop applications remains an option, though the use cases for this are quite niche. If your project was better suited as a desktop app from the outset,
perhaps Django wasn't the appropriate tool to begin with.

This is my perspective:

- You want to build a desktop app, not as an add-on or bonus feature for your existing web app.
- You are familiar with Django and do not wish to learn a new tool.

If these two conditions ring true, then this option makes sense — especially if you want to provide your users the flexibility to run your project on their computers with their data, without reliance on a server.

I've emphasized on desktop applications, and for good reason — the mobile aspect might not be worth the effort. How often do you install apps from unfamiliar sources on your phone these days? Exactly.

There are numerous options for creating desktop apps, but I recommend `beeware <https://docs.beeware.org/en/latest/>`_. According to their official documentation:

   "BeeWare is not a single product, or tool, or library - it’s a collection of tools and libraries, each of which works together to help you write cross-platform Python applications with a native GUI."

   -- `BeeWare Official docs <https://docs.beeware.org/en/latest/>`_

For an example on how to use BeeWare, you can check out this talk: `Let's build a BeeWare app that uses Django with Cheuk Ting Ho <https://www.youtube.com/watch?v=wAExEfkcY1U>`_.

Some alternatives to BeeWare are:

- `shiv <https://github.com/linkedin/shiv>`_ (For an introduction, consider reading `this insightful article <https://www.mattlayman.com/blog/2019/python-alternative-docker/>`_)
- `pyinstaller <https://www.pyinstaller.org/>`_
- `pyapp <https://github.com/ofek/pyapp>`_
- `nuitka <https://nuitka.net/>`_


The End
-------

Feeling overwhelmed? That's okay. If you're confused, then perhaps I didn't explain things as well as I could have. Your `feedback <https://github.com/tobi-de/falco/discussions>`_ is greatly appreciated.
The main goal of this guide was not to showcase specific deployment strategies, but to explain the key concepts of deployment. Regardless of the strategy you choose, there will almost always be a web server,
an application server, and a database. Some components may be hidden or abstracted away, but they are typically present in some form. Understanding these key concepts will help you navigate the landscape of deployment more easily.

.. admonition:: What should I do now?
   :class: hint dropdown

   If you're a beginner and unsure of what to do next, head over to `myjourney <https://github.com/Tobi-De/myjourney>`_ and try to deploy it :)
