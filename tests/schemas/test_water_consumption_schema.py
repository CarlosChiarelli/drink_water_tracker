from datetime import date

import pytest
from pydantic import ValidationError

from drink_water_tracker.schemas.cup_size import CupSize
from drink_water_tracker.schemas.user import User
from drink_water_tracker.schemas.water_consumption import (
    WaterConsumption,
    WaterConsumptionInput,
    WaterConsumptionOutput,
)


def test_water_consumption_schema():
    water_consumption = WaterConsumption(drink_date="2024-02-20")

    assert water_consumption.dict() == {"drink_date": date(2024, 2, 20)}


def test_water_consumption_schema_invalid_drink_date():
    with pytest.raises(ValidationError):
        water_consumption = WaterConsumption(drink_date="20/02/2024")  # noqa: F841


def test_water_consumption_input_schema():
    water_consumption = WaterConsumption(drink_date="2024-02-21")
    water_consumption_input = WaterConsumptionInput(
        user_id=1, cup_size_id=1, water_consumption=water_consumption
    )

    assert water_consumption_input.dict() == {
        "user_id": 1,
        "cup_size_id": 1,
        "water_consumption": {"drink_date": date(2024, 2, 21)},
    }


def test_water_consumption_output_schema():
    user = User(name="Carlos", weight=70)
    cup_size = CupSize(description="Copo pequeno 200mL", amount_ml=200)
    water_consumption_output = WaterConsumptionOutput(
        id=1, drink_date="2024-02-21", user=user, cup_size=cup_size
    )

    assert water_consumption_output.dict() == {
        "id": 1,
        "drink_date": date(2024, 2, 21),
        "user": {"name": "Carlos", "weight": 70},
        "cup_size": {"description": "Copo pequeno 200mL", "amount_ml": 200},
    }
