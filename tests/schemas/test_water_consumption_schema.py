from datetime import date, timedelta

import pytest
from pydantic import ValidationError

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
    water_consumption_output = WaterConsumptionOutput(
        consumption_date=today_str,
        day_goal_ml=2100,
        remaining_goal_ml=2100,
        consumed_goal_ml=0,
        consumed_goal_percentage=0,
        total_consumption_ml=0,
        goal_reached=False,
    )

    assert water_consumption_output.dict() == {
        "consumption_date": today,
        "day_goal_ml": 2100,
        "remaining_goal_ml": 2100,
        "consumed_goal_ml": 0,
        "consumed_goal_percentage": 0,
        "total_consumption_ml": 0,
        "goal_reached": False,
    }
