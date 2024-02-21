from datetime import date

from drink_water_tracker.schemas.base import CustomBaseModel
from drink_water_tracker.schemas.cup_size import CupSize
from drink_water_tracker.schemas.user import User


class WaterConsumption(CustomBaseModel):
    drink_date: date


class WaterConsumptionInput(CustomBaseModel):
    user_id: int
    cup_size_id: int
    water_consumption: WaterConsumption


class WaterConsumptionOutput(WaterConsumption):
    id: int
    user: User
    cup_size: CupSize
