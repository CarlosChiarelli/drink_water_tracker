from drink_water_tracker.db.models import User as UserModel
from drink_water_tracker.schemas.user import User
from drink_water_tracker.use_cases.user import UserUseCases


def test_add_user_uc(db_session):
    uc = UserUseCases(db_session)
    user = User(name="Carlos", weight=70)
    uc.add_user(user=user)
    users_on_db = db_session.query(UserModel).all()
    assert len(users_on_db) == 1
    assert users_on_db[0].name == "Carlos"
    assert users_on_db[0].weight == 70

    db_session.delete(users_on_db[0])
    db_session.commit()
