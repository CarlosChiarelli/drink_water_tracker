from sqlalchemy.orm import Session

from drink_water_tracker.db.models import CupSize as CupSizeModel
from drink_water_tracker.schemas.cup_size import CupSize, CupSizeOutput


class CupSizeUseCases:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def add_cup_size(self, cup_size: CupSize):
        cup_size_model = CupSizeModel(**cup_size.dict())
        self.db_session.add(cup_size_model)
        self.db_session.commit()

    def list_cup_sizes(self):
        cup_sizes_on_db = self.db_session.query(CupSizeModel).all()
        cup_sizes_output = [
            self.serialize_cup_size(cup_size_model) for cup_size_model in cup_sizes_on_db
        ]
        return cup_sizes_output

    def serialize_cup_size(self, cup_size_model: CupSizeModel):
        return CupSizeOutput(**cup_size_model.__dict__)
