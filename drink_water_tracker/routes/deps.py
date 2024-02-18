from drink_water_tracker.db.connection import Session


def get_db_session():
    try:
        session = Session()
        yield session
    finally:
        session.close()
