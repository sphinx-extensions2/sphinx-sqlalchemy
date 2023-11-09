sphinx-sqlalchemy
=================

Sphinx extension for documenting SQLAlchemy ORMs.

Usage
-----

Install ``sphinx_sqlalchemy``:

.. code-block:: bash

    pip install sphinx_sqlalchemy

Add ``sphinx_sqlalchemy`` to your ``conf.py``:

.. code-block:: python

    extensions = [
        'sphinx_sqlalchemy',
    ]

Example
-------

::

    .. sqla-model:: example.models.User

    .. sqla-model:: ~example.models.Address


.. sqla-model:: example.models.User

.. sqla-model:: ~example.models.Address

This was created from:

.. literalinclude:: example/models.py
    :lines: 1-
