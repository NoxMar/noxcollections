noxcollections
==============

simple, clean, pure python collections
---------------------------------------

**noxcollections** is pure Python implementation of basic data structures and a
few basic algorithms operating on them.

Disclaimer
==========

This project's main purpose is to get myself acquainted to the process of
developing a proper python package with the common tooling used for testing,
linting, type checking, and building in python.

Additionally I hope to refresh and better structure my knowledge about the
implemented data structures and algorithms.

For the reasons stated above this project is mainly meant for educational
purposes. **If you need performance built-in package** ``collections`` **as well
as some other packages from PyPI will probably serve you better** (due to better
optimization as well as the fact that most of them are implemented as C
extensions).

Goals
=====

Following goals are most important to this project:

- Clean, modern code
- Full test coverage
- Fully typed public API

Current state
=============

The following lists contain planned features and their state current state.

This package is currently before its first release. 

Data structures
---------------

- [ ] Linked lists and other data structures that can be based on them
    - [x] Linked list
    - [ ] Doubly linked list
    - [x] Stack
    - [ ] Queues
- [ ] Other list types
- [ ] Tree based structures
- [ ] Graphs based structures

Algorithms
----------

- [x] Search Algorithms
    - [x] Binary search
    - [x] Linear search
- [ ] Sorting Algorithms
    - [x] Bubble sort
    - [x] Merge sort 
    - [ ] Quick sort
- [ ] Graph algorithms (TBD)

How to use
==========

For use only Python(``3.8+``) interpreter is needed. To run test/linters/mypy
use of Poetry_ is recommended. Further instructions will assume you have it 
installed.

.. _Poetry: https://python-poetry.org/

Installation
------------

Install using pip
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can install last release version of this package from PyPI_ using ``pip``.

.. code-block:: bash

    pip install noxcollections

.. _PyPi: https://pypi.org/project/noxcollections/

Using Poetry
------------

First install the package in the environment manage by Poetry:

.. code-block:: bash

    poetry install  # build, from main repository directory

And then call your script from the main repository's directory prefacing it 
with ``poetry`` for example if your file is int same directory and as called
``main.py``::

    poetry python main.py

Testing and linting
===================

Testing uses the pytest_ package for testing and tox_ to run the test suite
against multiple versions of Python:

- ``3.8``
- ``3.9``
- ``3.10``

Tox configurations also does linting (using black_ and flake8_) and type
checking (using mypy_)

To run all of the aforementioned tools using tox (after installing all of the 
dependencies and package using ``poetry install``)::

    poetry run tox

To run those tools more selectively check the ``tox.ini`` file to check the names
of the environments you wish to run.

.. _pytest: https://pytest.org/
.. _tox: https://tox.wiki/
.. _black: https://pypi.org/project/black/
.. _flake8: https://flake8.pycqa.org/
.. _mypy: http://www.mypy-lang.org/