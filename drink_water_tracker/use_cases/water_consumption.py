from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from drink_water_tracker.db.models import CupSize as CupSizeModel
from drink_water_tracker.db.models import User as UserModel
from drink_water_tracker.db.models import WaterConsumption as WaterConsumptionModel
from drink_water_tracker.schemas.water_consumption import WaterConsumption


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
