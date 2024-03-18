:image: https://raw.githubusercontent.com/Tobi-De/falco/main/assets/og-image.jpg
:description: permissions and authorizations

Permissions and authorizations
==============================

.. warning::

    Work in progress. To receive updates `subscribe to this discussion <https://github.com/Tobi-De/falco/discussions/39>`_ or
    follow me on `x <https://twitter.com/tobidegnon>`_ or `mastodon <https://fosstodon.org/@tobide>`_.

What is permissions and authorizations?
---------------------------------------


The options to implement them in django
---------------------------------------

When do you need to build a custom permissions and authorization system? Spoiler **hardly ever**.

- You have Linux Torvalds-level technical skills in software development.
- Your use case is truly unique, nobody has ever done it before.
- You have abundant resources at your disposal, including time, money, and people.
- It is not a serious project, but rather an opportunity to learn new things.

If at least two of these conditions are not true at the same time, please do not build a custom permissions and authorization system.
Instead, use a proven and maintained solution. Building this stuff is hard, very hard, and even harder to maintain.

    Everyone knows that debugging is twice as hard as writing a program in the first place. So if you’re as clever as you can be when you write it,
    how will you ever debug it?

    -- Brian Kernighan, 1974

.. admonition:: A rephrased version of the quote above that I like more
    :class: hint dropdown

    Debugging is twice as hard as writing the code in the first place. Therefore, if you write the code as cleverly as possible, you are,
    by definition, not smart enough to debug it.


In my experience, you can swap **debug** with **maintain** and it will still be true.

Before considering the options below, I'll assume that you first tried the `Django integrated permissions system <https://docs.djangoproject.com/en/5.0/topics/auth/default/#topic-authorization>`_ and
it was not enough for your use case.

Django packages
^^^^^^^^^^^^^^^

* https://djangopackages.org/grids/g/perms/
* https://djangopackages.org/grids/g/authorization/

Role based

https://github.com/vintasoftware/django-role-permissions

Content based

https://github.com/dfunckt/django-rules
https://github.com/django-guardian/django-guardian



P.A.A.S solutions
^^^^^^^^^^^^^^^^^

* https://github.com/goauthentik/authentik
* https://github.com/open-policy-agent/opa
* https://github.com/zitadel/zitadel
