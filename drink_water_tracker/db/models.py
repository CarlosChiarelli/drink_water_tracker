from sqlalchemy import Column, Integer, Numeric, String

from drink_water_tracker.db.base import Base


class User(Base):
    __tablename__ = "user"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(50), nullable=False)
    weight = Column("weight", Numeric(precision=5, scale=2))
