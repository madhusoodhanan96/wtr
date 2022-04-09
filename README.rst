===
wtr
===

``wtr`` is a command-line weather application.


Developing
==========

Prerequisites
-------------

* Python 3.10.
* `tox <https://tox.wiki/en/latest/>`_.
* `pre-commit <https://pre-commit.com/>`_.

Usage
-----

Install the ``wtr`` project in editable mode inside a ``virtualenv`` environment.

  .. code:: bash

    $ cd <top-level directory of this repository>
    $ python3 -m venv venv
    $ . venv/bin/activate
    $ pip install -e .
    $ wtr

List the available ``tox`` environments.

  .. code:: bash

    $ tox -lv
    default environments:
    py310    -> run the test suite
    lint     -> run the linters
    coverage -> generate coverage report

Run the project's tests.

  .. code:: bash

    $ tox -e py310

Since ``tox`` uses `pytest <https://docs.pytest.org/>`_ under the hood to run
the tests, arguments can be passed to ``pytest``.

  .. code:: bash

    $ tox -e py310 -- path/to/test/file.py  # Run the tests in a specific file.
    $ tox -e py310 -- -k test_foo_bar  # Pattern for the tests to run.
    $ tox -e py310 -- --lf  # Run the tests that failed the last time.

Run the tests with coverage.

  .. code:: bash

    $ tox -e coverage

Run the linters.

  .. code:: bash

    $ tox -e lint

We also support running linters via `pre-commit <https://pre-commit.com/>`_.
If you want ``pre-commit`` to run automatically on ``git commit``,
you need to run ``pre-commit install`` once.


Getting help
------------

If you find bugs in this application, you can report them here:

    https://github.com/madhusoodhanan96/wtr
