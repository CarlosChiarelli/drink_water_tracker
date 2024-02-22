from datetime import date, timedelta

import pytest
from fastapi.exceptions import HTTPException

from drink_water_tracker.db.models import WaterConsumption as WaterConsumptionModel
from drink_water_tracker.schemas.water_consumption import (
    WaterConsumption,
    WaterConsumptionOutput,
)
from drink_water_tracker.use_cases.water_consumption import WaterConsumptionUseCases

yesterday = date.today() - timedelta(days=1)
yesterday_str = yesterday.strftime("%Y-%m-%d")


def test_add_water_consumption_uc(db_session, users_on_db, cup_sizes_on_db):
    uc = WaterConsumptionUseCases(db_session)
    water_consumption = WaterConsumption(drink_date=yesterday_str)
    uc.add_water_consumption(
        water_consumption=water_consumption,
        user_id=users_on_db[0].id,
        cup_size_id=cup_sizes_on_db[0].id,
    )
    water_consumption_on_db = db_session.query(WaterConsumptionModel).first()

    assert water_consumption_on_db is not None
    assert water_consumption_on_db.drink_date == water_consumption.drink_date
    assert water_consumption_on_db.user.name == users_on_db[0].name
    assert water_consumption_on_db.user.weight == users_on_db[0].weight
    assert water_consumption_on_db.cup_size.description == cup_sizes_on_db[0].description
    assert water_consumption_on_db.cup_size.amount_ml == cup_sizes_on_db[0].amount_ml

    db_session.delete(water_consumption_on_db)
    db_session.commit()


def test_add_water_consumption_invalid_user(db_session, users_on_db, cup_sizes_on_db):
    uc = WaterConsumptionUseCases(db_session)
    water_consumption = WaterConsumption(drink_date=yesterday_str)

    with pytest.raises(HTTPException):
        uc.add_water_consumption(
            water_consumption=water_consumption,
            user_id=-1,
            cup_size_id=cup_sizes_on_db[0].id,
        )


def test_add_water_consumption_invalid_cup_size(db_session, users_on_db, cup_sizes_on_db):
    uc = WaterConsumptionUseCases(db_session)
    water_consumption = WaterConsumption(drink_date=yesterday_str)

    with pytest.raises(HTTPException):
        uc.add_water_consumption(
            water_consumption=water_consumption,
            user_id=users_on_db[0].id,
            cup_size_id=-1,
        )


def test_list_water_consumption(db_session, water_consumption_on_db):
    uc = WaterConsumptionUseCases(db_session=db_session)
    water_consumption = uc.list_water_consumption()

    for wtcmp in water_consumption_on_db:
        db_session.refresh(wtcmp)

    assert len(water_consumption) == 8
    assert type(water_consumption[0]) is WaterConsumptionOutput
    assert water_consumption[0].drink_date == water_consumption_on_db[0].drink_date
    assert water_consumption[0].user.name == water_consumption_on_db[0].user.name
    assert water_consumption[0].user.weight == water_consumption_on_db[0].user.weight
    assert (
        water_consumption[0].cup_size.description
        == water_consumption_on_db[0].cup_size.description
    )
    assert (
        water_consumption[0].cup_size.amount_ml
        == water_consumption_on_db[0].cup_size.amount_ml
    )


def test_filter_water_consumption_by_username_and_date(
    db_session, water_consumption_on_db
):
    uc = WaterConsumptionUseCases(db_session=db_session)
    water_consumption = uc.list_water_consumption(
        user_name="Carlos", drink_date=yesterday_str
    )

    for wtcmp_on_db in water_consumption_on_db:
        db_session.refresh(wtcmp_on_db)

    assert len(water_consumption) == 4
    assert type(water_consumption[0]) is WaterConsumptionOutput
    assert all(item.user.name == "Carlos" for item in water_consumption)
    assert all(item.drink_date == yesterday for item in water_consumption)


def test_filter_water_consumption_by_username(db_session, water_consumption_on_db):
    uc = WaterConsumptionUseCases(db_session=db_session)
    water_consumption = uc.list_water_consumption(user_name="Carlos")

    for wtcmp_on_db in water_consumption_on_db:
        db_session.refresh(wtcmp_on_db)

    assert len(water_consumption) == 5
    assert type(water_consumption[0]) is WaterConsumptionOutput
    assert all(item.user.name == "Carlos" for item in water_consumption)
