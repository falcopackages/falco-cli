:image: https://raw.githubusercontent.com/Tobi-De/falco/main/assets/og-image.jpg
:description: A guide on some common database pattern and strategies and how to use them with django.

Database Tips: Backup, Scaling, Triggers, and More
==================================================

.. warning::

    Work in progress. To receive updates `subscribe to this discussion <https://github.com/Tobi-De/falco/discussions/39>`_ or
    follow me on `x <https://twitter.com/tobidegnon>`_ or `mastodon <https://fosstodon.org/@tobide>`_.

django-pgtriggers
-----------------

Database backup
---------------

Whenever possible, take advantage of a fully managed database solution, they usually offer automatic backup of your databases.
In my opinion, this is the best option if you don’t want to deal with the hassle of managing your own database.

-  `Amazon RDS <https://aws.amazon.com/rds/>`__
-  `Linode Managed Databases <https://www.linode.com/products/databases/>`__
-  `DigitalOcean Managed Databases <https://www.digitalocean.com/products/managed-databases>`__
-  `Heroku postgres <https://www.heroku.com/postgres>`__

For specific postgresql options, see their `hosting support page <https://www.postgresql.org/support/professional_hosting/>`__.

However, if for some reason you want / need to manage your database yourself and just want an automatic backup solution
then `django-dbbackup <https://github.com/jazzband/django-dbbackup>`__ is what you need. You can use one of the scheduling
packages discussed above to periodically run the backup command.

Scaling strategies
------------------

This is mostly a buzzword, people use that term to represent an app that can handle thousands or millions of requests per second.
Scalability is a problem you want to have (that means you've made it), but people are out there solving scalability issues for
apps that have not even been shipped, like a `classic chicken and egg <https://en.wikipedia.org/wiki/Chicken_or_the_egg>`_ problem.
I don't have enough personal experience here to give good advice, but I'll try to provide some pointers based on what I've read and
the little experience I have (apps I've seen even if I haven't worked on them).
I put this section here (in the databases guide) because it seems that more often than not, the database is the bottleneck, or at least
before Django or Python become a bottleneck for you, your database will be the first to become a bottleneck. Maybe not the database itself at
first, but how you access it and how your queries are written. For more on that, check out the `database optimization section </guides/optimizing_database_access.html>`__.
Both of these sections are complementary.

For most of these strategies, I'll assume you are using PostgreSQL because that's what I know best, but most of these strategies can be applied to other databases.


Offload work from the database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Table partitionning
^^^^^^^^^^^^^^^^^^^

Read replicas
^^^^^^^^^^^^^

Sharding
^^^^^^^^
