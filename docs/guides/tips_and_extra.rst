:description: Things that does not deserve a full guide or I don’t know where to put them.

Tips and extra
==============

Things that does not deserve a full guide or I don’t know where to put them.


Understanding django Settings
-----------------------------

If there is a setting in ``settings.py`` or elsewhere that you don’t understand, go to the `official django settings reference page <https://docs.djangoproject.com/en/dev/ref/settings/>`__
and press Ctrl + F to search for it. I used the `django-production <https://github.com/lincolnloop/django-production>`__ package to configure the production settings which I then customized.
I have removed the package as a dependency, but I advise you to go and check for yourself what is available.

Local email testing
--------------------

https://github.com/axllent/mailpit


Lifecycle not signals
---------------------


Avoid huge apps for large projects
----------------------------------

Generate admin
--------------

https://django-extensions.readthedocs.io/en/latest/admin_generator.html

Auto Fill forms
---------------

Fake filler
