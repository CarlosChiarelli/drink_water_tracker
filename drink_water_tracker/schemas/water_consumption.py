from datetime import date

from drink_water_tracker.schemas.base import CustomBaseModel


class WaterConsumption(CustomBaseModel):
    drink_date: date


class WaterConsumptionInput(CustomBaseModel):
    user_id: int
    cup_size_id: int
    water_consumption: WaterConsumption


class WaterConsumptionOutput(CustomBaseModel):
    consumption_date: date
    day_goal_ml: float
    remaining_goal_ml: float
    consumed_goal_ml: float
    consumed_goal_percentage: float
    total_consumption_ml: float
    goal_reached: bool
