import pytest

from drink_water_tracker.db.connection import Session
from drink_water_tracker.db.models import CupSize as CupSizeModels


@pytest.fixture
def db_session():
    try:
        session = Session()
        yield session
    finally:
        session.close()


@pytest.fixture
def cup_sizes_on_db(db_session):
    cup_sizes = [
        CupSizeModels(description="Copo pequeno 250mL", amount_ml=250),
        CupSizeModels(description="Copo médio 350mL", amount_ml=350),
        CupSizeModels(description="Garrafa média 500mL", amount_ml=500),
        CupSizeModels(description="Garrafa grande 750mL", amount_ml=750),
    ]

    for cup_size in cup_sizes:
        db_session.add(cup_size)
    db_session.commit()

    # update the ID in the object
    for cup_size in cup_sizes:
        db_session.refresh(cup_size)

    yield cup_sizes

    for cup_size in cup_sizes:
        db_session.delete(cup_size)
    db_session.commit()
