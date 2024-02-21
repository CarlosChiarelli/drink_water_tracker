from datetime import date

from drink_water_tracker.schemas.base import CustomBaseModel


class WaterConsumption(CustomBaseModel):
    drink_date: date


class WaterConsumptionInput(CustomBaseModel):
    user_id: int
    cup_size_id: int
    water_consumption: WaterConsumption
