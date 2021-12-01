sphinx-sqlalchemy
=================

Sphinx extension for documenting SQLAlchemy ORMs.

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
