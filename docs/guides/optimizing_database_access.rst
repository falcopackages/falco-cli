:image: https://raw.githubusercontent.com/Tobi-De/falco/main/assets/og-image.jpg
:description: Optimizing Database Access in django

Optimizing Database Access
==========================

.. warning::

    Work in progress. To receive updates `subscribe to this discussion <https://github.com/Tobi-De/falco/discussions/39>`_ or
    follow me on `x <https://twitter.com/tobidegnon>`_ or `mastodon <https://fosstodon.org/@tobide>`_.

https://github.com/Jdsleppy/django-orm-cheatsheet


I'll asume you are using PostgreSQL, but most of the tips are valid for other databases too.

Always profile first
--------------------



Select and prefetch related
---------------------------

Defer and only
--------------

Do the work early
---------------------

Caching with Redis
-------------------

https://github.com/Suor/django-cacheops
https://github.com/noripyt/django-cachalot


Using indexes
-------------

Materialized views
------------------

Denormalization
---------------

Cursor based pagination
-----------------------
