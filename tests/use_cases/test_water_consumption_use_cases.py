import pytest
from fastapi.exceptions import HTTPException

from drink_water_tracker.db.models import WaterConsumption as WaterConsumptionModel
from drink_water_tracker.schemas.water_consumption import WaterConsumption
from drink_water_tracker.use_cases.water_consumption import WaterConsumptionUseCases


def test_add_water_consumption_uc(db_session, users_on_db, cup_sizes_on_db):
    uc = WaterConsumptionUseCases(db_session)
    water_consumption = WaterConsumption(drink_date="2024-02-20")
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
    water_consumption = WaterConsumption(drink_date="2024-02-20")

    with pytest.raises(HTTPException):
        uc.add_water_consumption(
            water_consumption=water_consumption,
            user_id=-1,
            cup_size_id=cup_sizes_on_db[0].id,
        )


def test_add_water_consumption_invalid_cup_size(db_session, users_on_db, cup_sizes_on_db):
    uc = WaterConsumptionUseCases(db_session)
    water_consumption = WaterConsumption(drink_date="2024-02-20")

    with pytest.raises(HTTPException):
        uc.add_water_consumption(
            water_consumption=water_consumption,
            user_id=users_on_db[0].id,
            cup_size_id=-1,
        )
