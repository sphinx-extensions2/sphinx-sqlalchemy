from sqlalchemy import Column, UniqueConstraint, orm, types

Base = orm.declarative_base()


class TestUserMultilineDocstringD212(Base):
    """
    A ``user``.

    The user has a multi-line docstring::

        This is an indented code block

    This is the last line of the docstring.
    """

    __tablename__ = "dbusers_d212"
    __table_args__ = (UniqueConstraint("first_name", "last_name"),)
    pk = Column(types.Integer, primary_key=True)
    first_name = Column(types.String, doc="The name of the user.")
    last_name = Column(types.String(255), doc="The surname of the user.")
    dob = Column(types.Date, nullable=False, doc="The date of birth.")


class TestUserMultilineDocstringD213(Base):
    """A ``user``.

    The user has a multi-line docstring::

        This is an indented code block

    This is the last line of the docstring.
    """

    __tablename__ = "dbusers_d213"
    __table_args__ = (UniqueConstraint("first_name", "last_name"),)
    pk = Column(types.Integer, primary_key=True)
    first_name = Column(types.String, doc="The name of the user.")
    last_name = Column(types.String(255), doc="The surname of the user.")
    dob = Column(types.Date, nullable=False, doc="The date of birth.")
