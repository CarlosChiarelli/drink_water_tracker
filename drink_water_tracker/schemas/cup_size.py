from drink_water_tracker.schemas.base import CustomBaseModel


class CupSize(CustomBaseModel):
    description: str
    amount_ml: float


class CupSizeOutput(CupSize):
    id: int
