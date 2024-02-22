from datetime import date, timedelta

import pytest
from fastapi.exceptions import HTTPException

from drink_water_tracker.db.models import WaterConsumption as WaterConsumptionModel
from drink_water_tracker.schemas.water_consumption import (
    WaterConsumption,
    WaterConsumptionOutput,
)
from drink_water_tracker.use_cases.water_consumption import WaterConsumptionUseCases

today = date.today()
today_str = today.strftime("%Y-%m-%d")
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


def test_add_water_consumption_invalid_user_uc(db_session, users_on_db, cup_sizes_on_db):
    uc = WaterConsumptionUseCases(db_session)
    water_consumption = WaterConsumption(drink_date=yesterday_str)

    with pytest.raises(HTTPException):
        uc.add_water_consumption(
            water_consumption=water_consumption,
            user_id=-1,
            cup_size_id=cup_sizes_on_db[0].id,
        )


def test_add_water_consumption_invalid_cup_size_uc(
    db_session, users_on_db, cup_sizes_on_db
):
    uc = WaterConsumptionUseCases(db_session)
    water_consumption = WaterConsumption(drink_date=yesterday_str)

    with pytest.raises(HTTPException):
        uc.add_water_consumption(
            water_consumption=water_consumption,
            user_id=users_on_db[0].id,
            cup_size_id=-1,
        )


def test_list_water_consumption_by_username_uc(
    db_session, water_consumption_multiple_users_on_db
):
    uc = WaterConsumptionUseCases(db_session=db_session)
    water_consumption = uc.list_water_consumption(user_name="Carlos")

    for wc in water_consumption_multiple_users_on_db:
        db_session.refresh(wc)

    assert len(water_consumption) == 2
    assert type(water_consumption[0]) is WaterConsumptionOutput
    assert type(water_consumption[1]) is WaterConsumptionOutput

    assert water_consumption[0].consumption_date == yesterday
    assert water_consumption[0].day_goal_ml == 2450
    assert water_consumption[0].remaining_goal_ml == 0
    assert water_consumption[0].consumed_goal_ml == 2450
    assert water_consumption[0].consumed_goal_percentage == 100
    assert water_consumption[0].total_consumption_ml == 3000
    assert water_consumption[0].goal_reached is True

    assert water_consumption[1].consumption_date == today
    assert water_consumption[1].day_goal_ml == 2450
    assert water_consumption[1].remaining_goal_ml == 2100
    assert water_consumption[1].consumed_goal_ml == 350
    assert water_consumption[1].consumed_goal_percentage == 14.3
    assert water_consumption[1].total_consumption_ml == 350
    assert water_consumption[1].goal_reached is False


def test_list_water_consumption_by_username_and_date_uc(
    db_session, water_consumption_multiple_users_on_db
):
    uc = WaterConsumptionUseCases(db_session=db_session)
    water_consumption = uc.list_water_consumption(user_name="Maria", drink_date=yesterday)

    for wc in water_consumption_multiple_users_on_db:
        db_session.refresh(wc)

    assert len(water_consumption) == 1
    assert type(water_consumption[0]) is WaterConsumptionOutput

    assert water_consumption[0].consumption_date == yesterday
    assert water_consumption[0].day_goal_ml == 1925
    assert water_consumption[0].remaining_goal_ml == 1675
    assert water_consumption[0].consumed_goal_ml == 250
    assert water_consumption[0].consumed_goal_percentage == 13
    assert water_consumption[0].total_consumption_ml == 250
    assert water_consumption[0].goal_reached is False
