from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    func,
)
from sqlalchemy.orm import relationship

from drink_water_tracker.db.base import Base


class User(Base):
    __tablename__ = "user"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(50), nullable=False)
    weight = Column("weight", Numeric(precision=5, scale=2), nullable=False)

    water_consumption = relationship("WaterConsumption", back_populates="user")


class CupSize(Base):
    __tablename__ = "cup_size"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    description = Column("description", String(20), nullable=False)
    amount_ml = Column("amount_ml", Numeric(precision=6, scale=2), nullable=False)

    water_consumption = relationship("WaterConsumption", back_populates="cup_size")


class WaterConsumption(Base):
    __tablename__ = "water_consumption"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    drink_date = Column("drink_date", Date, nullable=False)
    created_at = Column("created_at", DateTime, server_default=func.now())
    user_id = Column("user_id", ForeignKey("user.id"), nullable=False)  # type: ignore
    cup_size_id = Column(
        "cup_size_id", ForeignKey("cup_size.id"), nullable=False
    )  # type: ignore

    user = relationship("User", back_populates="water_consumption")
    cup_size = relationship("CupSize", back_populates="water_consumption")
