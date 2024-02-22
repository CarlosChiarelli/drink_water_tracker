from datetime import date, timedelta

from fastapi import status
from fastapi.testclient import TestClient

from drink_water_tracker.db.models import User as UserModel
from drink_water_tracker.db.models import WaterConsumption as WaterConsumptionModel
from drink_water_tracker.main import app

client = TestClient(app)

yesterday_str = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
today_str = date.today().strftime("%Y-%m-%d")
tomorrow_str = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")


def test_add_water_consumption_route(db_session, users_on_db, cup_sizes_on_db):

    body = {
        "user_id": users_on_db[0].id,
        "cup_size_id": cup_sizes_on_db[0].id,
        "water_consumption": {"drink_date": yesterday_str},
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
        "water_consumption": {"drink_date": yesterday_str},
    }
    response = client.post("/water-consumption/add", json=body)

    assert response.status_code == status.HTTP_404_NOT_FOUND

    water_consumption_on_db = db_session.query(WaterConsumptionModel).all()

    assert len(water_consumption_on_db) == 0


def test_add_water_consumption_route_invalid_cup_size(db_session, users_on_db):
    body = {
        "user_id": users_on_db[0].id,
        "cup_size_id": -1,
        "water_consumption": {"drink_date": yesterday_str},
    }
    response = client.post("/water-consumption/add", json=body)

    assert response.status_code == status.HTTP_404_NOT_FOUND

    water_consumption_on_db = db_session.query(WaterConsumptionModel).all()

    assert len(water_consumption_on_db) == 0


def test_list_water_consumption_by_username_default_date_route(
    water_consumption_multiple_users_on_db,
):
    response = client.get("/water-consumption/list?username=Carlos")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert len(data) == 1
    assert data[0]["consumption_date"] == today_str
    assert data[0]["day_goal_ml"] == 2450
    assert data[0]["remaining_goal_ml"] == 2100
    assert data[0]["consumed_goal_ml"] == 350
    assert data[0]["consumed_goal_percentage"] == 14.3
    assert data[0]["total_consumption_ml"] == 350
    assert data[0]["goal_reached"] is False


def test_list_water_consumption_by_username_and_date_route(
    water_consumption_multiple_users_on_db,
):
    response = client.get(
        f"/water-consumption/list?username=Maria&drinkdate={yesterday_str}"
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert len(data) == 1
    assert data[0]["consumption_date"] == yesterday_str
    assert data[0]["day_goal_ml"] == 1925
    assert data[0]["remaining_goal_ml"] == 1675
    assert data[0]["consumed_goal_ml"] == 250
    assert data[0]["consumed_goal_percentage"] == 13
    assert data[0]["total_consumption_ml"] == 250
    assert data[0]["goal_reached"] is False


def test_list_water_consumption_by_username_route_without_user_parameter(
    db_session,
    water_consumption_multiple_users_on_db,
):
    response = client.get("/water-consumption/list")

    assert response.status_code == status.HTTP_404_NOT_FOUND

    water_consumption_on_db = (
        db_session.query(WaterConsumptionModel)
        .join(WaterConsumptionModel.user)
        .filter(UserModel.name == "")
        .all()
    )

    assert len(water_consumption_on_db) == 0


def test_list_water_consumption_by_username_route_invalid_user(
    db_session,
    water_consumption_multiple_users_on_db,
):
    name = "Elon Musk"
    response = client.get(f"/water-consumption/list?username={name}")

    assert response.status_code == status.HTTP_404_NOT_FOUND

    water_consumption_on_db = (
        db_session.query(WaterConsumptionModel)
        .join(WaterConsumptionModel.user)
        .filter(UserModel.name == name)
        .all()
    )

    assert len(water_consumption_on_db) == 0


def test_list_water_consumption_by_username_route_invalid_date(
    db_session,
    water_consumption_multiple_users_on_db,
):
    response = client.get(
        f"/water-consumption/list?username=Maria&drinkdate={tomorrow_str}"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    water_consumption_on_db = (
        db_session.query(WaterConsumptionModel)
        .join(WaterConsumptionModel.user)
        .filter(UserModel.name == "")
        .filter(WaterConsumptionModel.drink_date == tomorrow_str)
        .all()
    )

    assert len(water_consumption_on_db) == 0


def test_list_water_consumption_by_username_get_history_route(
    water_consumption_multiple_users_on_db,
):
    response = client.get("/water-consumption/list/all?username=Carlos")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert len(data) == 2

    assert data[0]["consumption_date"] == yesterday_str
    assert data[0]["day_goal_ml"] == 2450
    assert data[0]["remaining_goal_ml"] == 0
    assert data[0]["consumed_goal_ml"] == 2450
    assert data[0]["consumed_goal_percentage"] == 100
    assert data[0]["total_consumption_ml"] == 3000
    assert data[0]["goal_reached"] is True

    assert data[1]["consumption_date"] == today_str
    assert data[1]["day_goal_ml"] == 2450
    assert data[1]["remaining_goal_ml"] == 2100
    assert data[1]["consumed_goal_ml"] == 350
    assert data[1]["consumed_goal_percentage"] == 14.3
    assert data[1]["total_consumption_ml"] == 350
    assert data[1]["goal_reached"] is False
