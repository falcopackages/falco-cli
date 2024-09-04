:description: How to deploy a project generated with falco.

Deployment
==========


.. todo::

    Explain how deployment is configured for a project generated with falco

    - s8-overlay
    - caprover
    - postgres / litestream



.. deploying the project to caprover what is confugured by default, but you are free to change this, mode details on the `deployment guide </the_cli/start_project/deploy.html>`_.
.. build python wheel of your project, these a
.. create binary of your project using `pyapp <https://github.com/ofek/pyapp>`_ only for x86_64 linux, but you can easily add more platforms if needed.




.. The ``deploy`` folder contains some files that are needed for deployment, mainly docker related. If Docker isn't part of your deployment plan, this directory can be safely removed.
.. However, you might want to retain the ``gunicorn.conf.py`` file inside that directory, which is a basic Gunicorn configuration file that could be useful regardless of your chosen deployment strategy.

.. The project comes for docker and s6-overlay configuration for deployment. All deployment related files are in the ``deploy``folder.
.. s6-overay is an init service, uses for processes supervisation meant for
.. container. It is build around the s6 system. For more details on how s6-overlay check the dedicated guide on it.
.. All you need to known is  that the container produced by the image, is meant to run your django project using gunicorn and django-q2 for background tasks
.. and scheduling feature. For more details on django-q2 checkout the guides on task quues and schedulers in django.
