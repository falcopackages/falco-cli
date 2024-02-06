:image: https://raw.githubusercontent.com/Tobi-De/falco/main/assets/og-image.jpg
:description:

Running your project in a single container
==========================================

.. warning::

    Work in progress. To receive updates `subscribe to this discussion <https://github.com/Tobi-De/falco/discussions/39>`_ or
    follow me on `x <https://twitter.com/tobidegnon>`_ or `mastodon <https://fosstodon.org/@tobide>`_.

My mindset has always been aligned with the general consensus of one process per container. Therefore, the idea of running an entire Django project,
which may involve multiple services such as a web server, Redis, a task queue, a database etc. in a single container feels inherently
wrong to me. However, my skepticism was challenged after considering the reasoning provided by the s6-overlay team, which is why this guide exists. In
fact, I have previously experimented with this approach using supervisord in a one-off project without encountering any issues. Although I
do not claim it to be the best approach, I acknowledge that it can be a valid one and may make sense in certain scenarios, such as when you
need to quickly ship something to production while testing out an idea.

https://github.com/just-containers/s6-overlay
