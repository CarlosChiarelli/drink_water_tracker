from drink_water_tracker.db.models import CupSize as CupSizeModel
from drink_water_tracker.schemas.cup_size import CupSize, CupSizeOutput
from drink_water_tracker.use_cases.cup_size import CupSizeUseCases


def test_add_cup_size_uc(db_session):
    uc = CupSizeUseCases(db_session)
    cup_size = CupSize(description="Copo pequeno 250mL", amount_ml=250)
    uc.add_cup_size(cup_size=cup_size)
    cup_size_on_db = db_session.query(CupSizeModel).all()
    assert len(cup_size_on_db) == 1
    assert cup_size_on_db[0].description == "Copo pequeno 250mL"
    assert cup_size_on_db[0].amount_ml == 250

    db_session.delete(cup_size_on_db[0])
    db_session.commit()


def test_list_cup_sizes(db_session, cup_sizes_on_db):
    uc = CupSizeUseCases(db_session=db_session)
    cup_sizes = uc.list_cup_sizes()

    assert len(cup_sizes) == 4
    assert type(cup_sizes[0]) is CupSizeOutput
    assert cup_sizes[0].id == cup_sizes_on_db[0].id
    assert cup_sizes[0].description == cup_sizes_on_db[0].description
    assert cup_sizes[0].amount_ml == cup_sizes_on_db[0].amount_ml
