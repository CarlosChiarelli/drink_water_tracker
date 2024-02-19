import pytest

from drink_water_tracker.db.connection import Session


@pytest.fixture
def db_session():
    try:
        session = Session()
        yield session
    finally:
        session.close()
