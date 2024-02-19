import pytest

from drink_water_tracker.schemas.user import User


def test_user_schema():
    user = User(name="Carlos", weight=70)
    assert user.dict() == {"name": "Carlos", "weight": 70}


def test_user_schema_invalid_name():
    with pytest.raises(ValueError):
        User(name=27, weight=70)


def test_user_schema_invalid_weight():
    with pytest.raises(ValueError):
        User(name="Carlos", weight="seventy")
