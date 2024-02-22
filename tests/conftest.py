from datetime import date, timedelta

import pytest

from drink_water_tracker.db.connection import Session
from drink_water_tracker.db.models import CupSize as CupSizeModel
from drink_water_tracker.db.models import User as UserModel
from drink_water_tracker.db.models import WaterConsumption as WaterConsumptionModel


@pytest.fixture
def db_session():
    try:
        session = Session()
        yield session
    finally:
        session.close()


@pytest.fixture
def users_on_db(db_session):
    users = [
        UserModel(name="Carlos", weight=70),
        UserModel(name="Maria", weight=55),
    ]

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


# maybe remove
@pytest.fixture()
def water_consumption_multiple_users_on_db(db_session, users_on_db, cup_sizes_on_db):
    today = date.today().strftime("%Y-%m-%d")
    yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    carlos = users_on_db[0]
    maria = users_on_db[1]
    small_cup = cup_sizes_on_db[0]
    medium_cup = cup_sizes_on_db[1]
    large_bottle = cup_sizes_on_db[3]

    water_consumption = [
        WaterConsumptionModel(
            drink_date=yesterday,
            user_id=carlos.id,
            cup_size_id=large_bottle.id,
        ),
        WaterConsumptionModel(
            drink_date=yesterday,
            user_id=carlos.id,
            cup_size_id=large_bottle.id,
        ),
        WaterConsumptionModel(
            drink_date=yesterday,
            user_id=carlos.id,
            cup_size_id=large_bottle.id,
        ),
        WaterConsumptionModel(
            drink_date=yesterday,
            user_id=carlos.id,
            cup_size_id=large_bottle.id,
        ),
        WaterConsumptionModel(
            drink_date=yesterday,
            user_id=maria.id,
            cup_size_id=small_cup.id,
        ),
        WaterConsumptionModel(
            drink_date=today,
            user_id=carlos.id,
            cup_size_id=medium_cup.id,
        ),
        WaterConsumptionModel(
            drink_date=today,
            user_id=maria.id,
            cup_size_id=small_cup.id,
        ),
        WaterConsumptionModel(
            drink_date=today,
            user_id=maria.id,
            cup_size_id=medium_cup.id,
        ),
    ]
    for wc in water_consumption:
        db_session.add(wc)
    db_session.commit()

    # update the ID in the object
    for wc in water_consumption:
        db_session.refresh(wc)

    yield water_consumption

    for wc in water_consumption:
        db_session.delete(wc)
    db_session.commit()


@pytest.fixture()
def water_consumption_one_user_on_db(db_session, users_on_db, cup_sizes_on_db):
    today = date.today().strftime("%Y-%m-%d")
    yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    carlos = users_on_db[0]
    medium_cup = cup_sizes_on_db[1]
    large_bottle = cup_sizes_on_db[3]

    water_consumption = [
        WaterConsumptionModel(
            drink_date=yesterday,
            user_id=carlos.id,
            cup_size_id=large_bottle.id,
        ),
        WaterConsumptionModel(
            drink_date=yesterday,
            user_id=carlos.id,
            cup_size_id=large_bottle.id,
        ),
        WaterConsumptionModel(
            drink_date=yesterday,
            user_id=carlos.id,
            cup_size_id=large_bottle.id,
        ),
        WaterConsumptionModel(
            drink_date=yesterday,
            user_id=carlos.id,
            cup_size_id=large_bottle.id,
        ),
        WaterConsumptionModel(
            drink_date=today,
            user_id=carlos.id,
            cup_size_id=medium_cup.id,
        )
    ]
    for wc in water_consumption:
        db_session.add(wc)
    db_session.commit()

    # update the ID in the object
    for wc in water_consumption:
        db_session.refresh(wc)

    yield water_consumption

    for wc in water_consumption:
        db_session.delete(wc)
    db_session.commit()
