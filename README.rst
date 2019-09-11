===============================
Andela Eats API (WIP)
===============================

This Backend application serves as an API Backend to the AndelaEats application, which allows Andelans to pre-order lunch a day ahead.


Quickstart
----------

Run the following commands to bootstrap your environment ::

    $ git clone git@github.com:andela/andelaeats_api.git
    $ cd andelaeats_api/
    $ make up


Getting Started!
----------------

Ready to contribute? Here's how to set up `AndelaEatsApi` for local development.

1. Clone the `AndelaEatsApi` repo on GitHub::

    $ git clone git@github.com:andela/AndelaEatsApi.git

2. Install docker on your local machine. Assuming you have docker installed, this is how you set up your environment for local development::

    $ cd andelaeats_api/
    $ make up

    ---Using virtual env locally---
    $ cd andelaeats_api/
    $ python3 -m venv <env_name> && . venv/bin/activate
    $ pip install pip-tools
    $ pip install -r requirements.txt

    ---Incase new packages are installed---
    1. add packages to the requirements.in, then run
    $ pip-compile requirements.in

3. Additionally, you can run the tests with::

    $ make test

4. Create a feature branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the
   tests::

    $ make test

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website::



Coding Style Guide
------------------

Read through the [Google Python Style Guide](http://google.github.io/styleguide/pyguide.html)


Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.md.
3. Make sure that the tests pass before submitting a pull request.
4. The pull request should include at least 2 reviewers.


Shell
-----

To open the interactive shell, run ::

    $ make shell

By default, you will have access to the flask ``app``.


Running Tests/Linter
--------------------

To run all tests, run ::

    $ make test

To run the linter, run ::

    $ make lint

The ``lint`` command will attempt to fix any linting/style errors in the code. If you only want to know if the code will pass CI and do not wish for the linter to make changes, add the ``--check`` argument.


Tips
----

To see the available options::

    $ make help


Features of Andela Eats App
---------------------------

- View available meals
- View order history
- Rate a meal, vendor or engagement
- Order a meals

