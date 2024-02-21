from fastapi import status
from fastapi.testclient import TestClient

from drink_water_tracker.db.models import WaterConsumption as WaterConsumptionModel
from drink_water_tracker.main import app

client = TestClient(app)


def test_add_water_consumption_route(db_session, users_on_db, cup_sizes_on_db):
    body = {
        "user_id": users_on_db[0].id,
        "cup_size_id": cup_sizes_on_db[0].id,
        "water_consumption": {"drink_date": "2024-02-20"},
    }
    response = client.post("/water-consumption/add", json=body)

    assert response.status_code == status.HTTP_201_CREATED

    water_consumption_on_db = db_session.query(WaterConsumptionModel).all()

    assert len(water_consumption_on_db) == 1

    db_session.delete(water_consumption_on_db[0])
    db_session.commit()


def test_add_water_consumption_route_invalid_user(db_session, cup_sizes_on_db):
    body = {
        "user_id": -1,
        "cup_size_id": cup_sizes_on_db[0].id,
        "water_consumption": {"drink_date": "2024-02-20"},
    }
    response = client.post("/water-consumption/add", json=body)

    assert response.status_code == status.HTTP_404_NOT_FOUND

    water_consumption_on_db = db_session.query(WaterConsumptionModel).all()

    assert len(water_consumption_on_db) == 0


def test_add_water_consumption_route_invalid_cup_size(db_session, users_on_db):
    body = {
        "user_id": users_on_db[0].id,
        "cup_size_id": -1,
        "water_consumption": {"drink_date": "2024-02-20"},
    }
    response = client.post("/water-consumption/add", json=body)

    assert response.status_code == status.HTTP_404_NOT_FOUND

    water_consumption_on_db = db_session.query(WaterConsumptionModel).all()

    assert len(water_consumption_on_db) == 0
