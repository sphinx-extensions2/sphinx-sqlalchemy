from sqlalchemy import CheckConstraint, Column, UniqueConstraint, func, orm, types

Base = orm.declarative_base()


class TestUser(Base):
    """A ``user``."""

    __tablename__ = "dbusers"
    __table_args__ = (
        UniqueConstraint("first_name", "last_name"),
        CheckConstraint(
            func.length(func.trim("first_name")) > 0, "check_project_has_name"
        ),
    )
    pk = Column(types.Integer, primary_key=True)
    first_name = Column(types.String, doc="The name of the user.")
    last_name = Column(types.String(255), doc="The surname of the user.")
    dob = Column(types.Date, nullable=False, doc="The date of birth.")
