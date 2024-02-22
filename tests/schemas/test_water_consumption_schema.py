from datetime import date, timedelta

import pytest
from pydantic import ValidationError

from drink_water_tracker.schemas.cup_size import CupSize
from drink_water_tracker.schemas.user import User
from drink_water_tracker.schemas.water_consumption import (
    WaterConsumption,
    WaterConsumptionInput,
    WaterConsumptionOutput,
)

today = date.today()
today_str = today.strftime("%Y-%m-%d")
yesterday = date.today() - timedelta(days=1)
yesterday_str = yesterday.strftime("%Y-%m-%d")


def test_water_consumption_schema():
    water_consumption = WaterConsumption(drink_date=yesterday_str)
    assert water_consumption.dict() == {"drink_date": yesterday}


def test_water_consumption_schema_invalid_drink_date():
    with pytest.raises(ValidationError):
        water_consumption = WaterConsumption(drink_date="20/02/2024")  # noqa: F841


def test_water_consumption_input_schema():
    water_consumption = WaterConsumption(drink_date=today_str)
    water_consumption_input = WaterConsumptionInput(
        user_id=1, cup_size_id=1, water_consumption=water_consumption
    )

    assert water_consumption_input.dict() == {
        "user_id": 1,
        "cup_size_id": 1,
        "water_consumption": {"drink_date": today},
    }


def test_water_consumption_output_schema():
    user = User(name="Carlos", weight=70)
    cup_size = CupSize(description="Copo pequeno 200mL", amount_ml=200)
    water_consumption_output = WaterConsumptionOutput(
        id=1, drink_date=today_str, user=user, cup_size=cup_size
    )

    assert water_consumption_output.dict() == {
        "id": 1,
        "drink_date": today,
        "user": {"name": "Carlos", "weight": 70},
        "cup_size": {"description": "Copo pequeno 200mL", "amount_ml": 200},
    }
