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


def test_list_water_consumption_route(water_consumption_on_db):
    response = client.get("/water-consumption/list")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert len(data) == 8
    assert data[0] == {
        "id": water_consumption_on_db[0].id,
        "drink_date": str(water_consumption_on_db[0].drink_date),
        "user": {
            "name": water_consumption_on_db[0].user.name,
            "weight": water_consumption_on_db[0].user.weight,
        },
        "cup_size": {
            "description": water_consumption_on_db[0].cup_size.description,
            "amount_ml": water_consumption_on_db[0].cup_size.amount_ml,
        },
    }


def test_filter_water_consumption_by_username_and_date_route(water_consumption_on_db):
    response = client.get("/water-consumption/list?username=Carlos&drinkdate=2024-02-20")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert len(data) == 4
    assert all(item["user"]["name"] == "Carlos" for item in data)
    assert all(item["drink_date"] == "2024-02-20" for item in data)


def test_filter_water_consumption_by_username(water_consumption_on_db):
    response = client.get("/water-consumption/list?username=Carlos")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert len(data) == 5
    assert all(item["user"]["name"] == "Carlos" for item in data)
