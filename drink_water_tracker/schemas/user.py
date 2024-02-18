from drink_water_tracker.schemas.base import CustomBaseModel


class User(CustomBaseModel):
    name: str
    weight: float
