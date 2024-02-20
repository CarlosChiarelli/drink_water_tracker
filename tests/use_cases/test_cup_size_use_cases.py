from drink_water_tracker.schemas.cup_size import CupSizeOutput
from drink_water_tracker.use_cases.cup_size import CupSizeUseCases


def test_list_cup_sizes(db_session, cup_sizes_on_db):
    uc = CupSizeUseCases(db_session=db_session)
    cup_sizes = uc.list_cup_sizes()

    assert len(cup_sizes) == 4
    assert type(cup_sizes[0]) is CupSizeOutput
    assert cup_sizes[0].id == cup_sizes_on_db[0].id
    assert cup_sizes[0].description == cup_sizes_on_db[0].description
    assert cup_sizes[0].amount_ml == cup_sizes_on_db[0].amount_ml
