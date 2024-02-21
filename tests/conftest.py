import pytest

from drink_water_tracker.db.connection import Session
from drink_water_tracker.db.models import CupSize as CupSizeModel
from drink_water_tracker.db.models import User as UserModel


@pytest.fixture
def db_session():
    try:
        session = Session()
        yield session
    finally:
        session.close()


@pytest.fixture
def users_on_db(db_session):
    users = [UserModel(name="Carlos", weight=70), UserModel(name="Maria", weight=55)]

    for user in users:
        db_session.add(user)
    db_session.commit()

    # update the ID in the object
    for user in users:
        db_session.refresh(user)

    yield users

    for user in users:
        db_session.delete(user)
    db_session.commit()


@pytest.fixture
def cup_sizes_on_db(db_session):
    cup_sizes = [
        CupSizeModel(description="Copo pequeno 250mL", amount_ml=250),
        CupSizeModel(description="Copo médio 350mL", amount_ml=350),
        CupSizeModel(description="Garrafa média 500mL", amount_ml=500),
        CupSizeModel(description="Garrafa grande 750mL", amount_ml=750),
    ]

    for cup_size in cup_sizes:
        db_session.add(cup_size)
    db_session.commit()

    # update the ID in the object
    for cup_size in cup_sizes:
        db_session.refresh(cup_size)

    yield cup_sizes

    for cup_size in cup_sizes:
        db_session.delete(cup_size)
    db_session.commit()
