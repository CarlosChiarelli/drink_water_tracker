from datetime import date
from typing import Optional

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from drink_water_tracker.db.models import CupSize as CupSizeModel
from drink_water_tracker.db.models import User as UserModel
from drink_water_tracker.db.models import WaterConsumption as WaterConsumptionModel
from drink_water_tracker.schemas.water_consumption import (
    WaterConsumption,
    WaterConsumptionOutput,
)


class WaterConsumptionUseCases:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def add_water_consumption(
        self, water_consumption: WaterConsumption, user_id: int, cup_size_id: int
    ):
        user = self.db_session.query(UserModel).filter_by(id=user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No user was found with id {user_id}",
            )
        cup_size = self.db_session.query(CupSizeModel).filter_by(id=cup_size_id).first()
        if not cup_size:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No cup size was found with id {cup_size_id}",
            )
        water_consumption_model = WaterConsumptionModel(**water_consumption.dict())
        water_consumption_model.user_id = user.id
        water_consumption_model.cup_size_id = cup_size.id

        self.db_session.add(water_consumption_model)
        self.db_session.commit()

    def list_water_consumption(
        self, user_name: Optional[str] = None, drink_date: Optional[date] = None
    ):
        query = self.db_session.query(WaterConsumptionModel)

        if user_name:
            query = query.join(WaterConsumptionModel.user).filter(
                UserModel.name == user_name
            )
        if drink_date:
            query = query.filter(WaterConsumptionModel.drink_date == drink_date)

        water_consumption_on_db = query.all()
        water_consumption = [
            self._serialize_water_consumption(wtcmp) for wtcmp in water_consumption_on_db
        ]

        return water_consumption

    def _serialize_water_consumption(
        self, water_consumption_on_db: WaterConsumptionModel
    ):
        water_consumption_dict = water_consumption_on_db.__dict__
        water_consumption_dict["user"] = water_consumption_on_db.user.__dict__
        water_consumption_dict["cup_size"] = water_consumption_on_db.cup_size.__dict__

        return WaterConsumptionOutput(**water_consumption_dict)
