============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:


The Guides
----------

Contributions to the guides should be made via `GitHub Discussions <https://github.com/Tobi-De/falco/discussions>`_. Any
contribution is welcome, even for typos and grammatical errors. If a contribution requires a complete rewrite of a section or
an entire guide, or adds new insights (similar to an article review), proper credits will be given at the bottom of the relevant guide.
I will not accept any pull request that directly changes a guide without prior discussion on the topic, except for minor typo fixes.


The CLI
-------

Contributions to the CLI are more open. You can fix issues, suggest new commands, or propose improvements to existing ones.

Types of Contributions
^^^^^^^^^^^^^^^^^^^^^^

Report Bugs
***********

Report bugs at https://github.com/Tobi-De/falco/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
********

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
******************

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
*******************

falco could always use more documentation, whether as part of the
official falco docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
***************

The best way to send feedback is to file an issue at https://github.com/Tobi-De/falco/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
^^^^^^^^^^^^

Ready to contribute? Here's how to set up `falco` for local development.

1. Fork the `falco` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/falco.git --recurse-submodules

3. Install your local copy into a virtualenv. Assuming you have hatch installed, this is how you set up your fork for local development::

    $ cd falco/
    $ hatch env create

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

4. Install pre-commit hooks for linting and code formatting before every commit::

    $ pre-commit install

5. When you're done making changes, check that your changes pass tests including testing other Python versions::

    $ hatch run test

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
^^^^^^^^^^^^^^^^^^^^^^^

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Add the
   feature to the list in README.md.
3. The pull request should work for Python 3.10, 3.11 and 3.12. Check
   https://github.com/Tobi-De/falco/pulls
   and make sure that the tests pass for all supported Python versions.

Tips
^^^^

To run a subset of tests::

$ pytest tests/commands/test_htmx.py


Deploying
^^^^^^^^^

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.rst).
Then run::

$ hatch version patch # possible: major / minor / patch
$ git push
$ git push --tags
