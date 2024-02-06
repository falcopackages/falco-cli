:image: https://raw.githubusercontent.com/Tobi-De/falco/main/assets/og-image.jpg
:description: This is a collection of guides that address common issues in web development, specifically tailored to Django. Each guide provides solutions, patterns, and approaches that are relevant to Django projects.

Guides
======

.. warning::

    This whole section is still a work in progress. There is a lot of incomplete content and some of the content that is there is not yet polished.

This is a collection of guides that address common issues in web development, specifically tailored to Django. Each guide provides solutions,
patterns, and approaches that are relevant to Django projects.
It is similar to the `Django topic guides <https://docs.djangoproject.com/en/5.0/topics/>`_, but instead of focusing on components of the
framework like ``forms``, ``models``, ``views``, etc., it focuses on more general topics like ``task queues``, ``deployment``, ``realtime``, etc.

These guides are based on my own experience and are quite opinionated. For each guide, I will share my current approach (which may change with new experiences) for
tackling the issue at hand. I will also include alternatives so that you can make your own decision. The number of guides will be limited, as this is not a blog where I post anything and
everything (for that, check out my `blog <https://oluwatobi.dev/blog>`_). Instead, this is more like a collection of recipes for common problems.
If you have feedback on the content of any of the guides, please open a `new GitHub discussion <https://github.com/Tobi-De/falco/discussions>`_. Whether you think I'm wrong about something, have suggestions for improvement,
or have a better approach to solve a specific issue, I'll be happy to hear it.

.. note::
    I want to use GitHub discussions mostly for the guides part, and issues (broken code) for the CLI part.

Most  of the stuff here is aimed at folks who are somewhere between beginners and intermediate developers, leaning more towards the intermediate side. It's kinda assumed that you've done a couple of Django projects
(like the official `Django tutorial <https://docs.djangoproject.com/en/5.0/intro/tutorial01/>`_). I reckon you need to be pretty familiar with the framework to feel comfortable reading these guides. But hey,
I'll do my best to make them as easy to digest as possible and provide enough external resources for a deeper understanding.

External Ressources
-------------------

Before diving into the guides, here are my top recommendations for external resources that'll help you become a better django and web
developer in general.

**The obvious ones**

.. grid:: 1 1 1 2
    :class-row: surface
    :padding: 0
    :gutter: 2

    .. grid-item-card:: :octicon:`rocket` The official Django documentation
        :link: https://docs.djangoproject.com/en/dev/

        Django's documentation is arguably one of the best I have encountered. The **Topics guides** and **How-to guides** are particularly
        noteworthy and should not be overlooked.

    .. grid-item-card:: :octicon:`flame` The HTMX documentation
        :link: https://htmx.org/

        The htmx documentation have everything you need to understand htmx but they also have great essays that are worth reading
        to broader your understanding of web development.


**Programming principles**

.. grid:: 1 1 1 2
    :class-row: surface
    :padding: 0
    :gutter: 2

    .. grid-item-card:: :octicon:`zap` HTML First
        :link: https://html-first.com/

        HTML First is a set of principles that aims to make building web software easier, faster, more inclusive, and more maintainable.

    .. grid-item-card:: :octicon:`smiley` KISS
        :link: https://en.wikipedia.org/wiki/KISS_principle

        Keep it simple, stupid. This is a design principle that states that most systems work best if they are kept simple rather than made complicated.

    .. grid-item-card:: :octicon:`clock` WYAGNI
        :link: https://codeanthropology.substack.com/p/yagni-and-waygni?

        When Are You Gonna Need It? A look at how we reduce scope, what we lose along the way, and what we could gain if we didn't. With a short story from the startup trenches.

    .. grid-item-card:: :octicon:`gear` 12 Factor App
        :link: https://12factor.net/

        The twelve-factor app is a methodology for building software-as-a-service applications. These best practices are designed to enable applications to be built with portability and resilience when deployed to the web.


**Blog articles and videos**

.. grid:: 1 1 1 2
    :class-row: surface
    :padding: 0
    :gutter: 2

    .. grid-item-card:: :octicon:`book` Adam Johnson blog
        :link: https://adamj.eu/tech/

        A core Django developer, he provides comprehensive and unique content covering every aspect of the framework.

    .. grid-item-card:: :octicon:`video` BugBytes
        :link: https://www.youtube.com/bugbytes

        This is a great YouTube channel that provides a wealth of Django and HTMX content.


**The special ones**

.. grid:: 1 1 1 2
    :class-row: surface
    :padding: 0
    :gutter: 2

    .. grid-item-card:: :octicon:`book` The Grug Brained Developer
        :link: https://grugbrain.dev

        A layman's guide to thinking like the self-aware smol brained.

    .. grid-item-card:: :octicon:`shield-check` The Cult of Done
        :link: https://medium.com/@bre/the-cult-of-done-manifesto-724ca1c2ff13

        The cult of done manifesto is a set of principles that aims to help you get things done.



.. admonition:: Need Help with Django?
    :class: hint dropdown

    For general assistance with Django-related issues, visit the `Django Community <https://www.djangoproject.com/community/>`_ page.


.. toctree::
    :hidden:

    interactive_user_interfaces
    task_queues_and_schedulers
    writing_documentation
    writing_tests
    logging_and_monitoring
    deployment
    optimizing_database_access
    avoiding_god_models
    dynamic_model_schema
    realtime
    permissions_and_authorization
    database_tips
    multitenancy
    writing_async_code
    use_sqlite_in_production
    running_project_in_a_container
    tips_and_extra
