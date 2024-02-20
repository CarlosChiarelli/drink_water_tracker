import pytest

from drink_water_tracker.schemas.cup_size import CupSize


def test_cup_size_schema():
    cup_size = CupSize(description="Copo pequeno 250mL", amount_ml=250)
    assert cup_size.dict() == {"description": "Copo pequeno 250mL", "amount_ml": 250}


def test_cup_size_schema_invalid_description():
    with pytest.raises(ValueError):
        CupSize(description=100, amount_ml=250)


def test_cup_size_schema_invalid_amount_ml():
    with pytest.raises(ValueError):
        CupSize(description="Copo pequeno 250mL", amount_ml="mL")
