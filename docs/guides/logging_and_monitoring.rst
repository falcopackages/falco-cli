:image: https://raw.githubusercontent.com/Tobi-De/falco/main/assets/og-image.jpg
:description:

Logging and monitoring
======================

.. warning::

    Work in progress. To receive updates `subscribe to this discussion <https://github.com/Tobi-De/falco/discussions/39>`_ or
    follow me on `x <https://twitter.com/tobidegnon>`_ or `mastodon <https://fosstodon.org/@tobide>`_.


Health check your django project
--------------------------------

**Health check** is about making sure that your django application and related services are always available / running.
My go-to package for this is `django-health-check <https://github.com/revsys/django-health-check>`__.
After installing and configuring **django-health-check**, you need to associate it with an uptime monitoring service, this
is the service that will periodically call your **health-check** endpoint to make sure everything is fine.
Here is a list of available options.

-  `upptime <https://github.com/upptime/upptime>`__
-  `uptime-kuma <https://github.com/louislam/uptime-kuma>`__
-  `uptimerobot <https://uptimerobot.com/>`__
-  `better-uptime <https://betterstack.com/better-uptime>`__
-  `glitchtip <https://glitchtip.com/>`__

Read more on the health check pattern `here <https://learn.microsoft.com/en-us/azure/architecture/patterns/health-endpoint-monitoring>`__.
