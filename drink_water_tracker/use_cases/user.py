from sqlalchemy.orm import Session

from drink_water_tracker.db.models import User as UserModel
from drink_water_tracker.schemas.user import User


class UserUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_user(self, user: User):
        user_model = UserModel(**user.dict())
        self.db_session.add(user_model)
        self.db_session.commit()
