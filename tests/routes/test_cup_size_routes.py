from fastapi import status
from fastapi.testclient import TestClient

from drink_water_tracker.main import app

client = TestClient(app)


def test_list_cup_sizes_route(cup_sizes_on_db):
    response = client.get("/cup-size/list")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) == 4
    assert data[0] == {
        "id": cup_sizes_on_db[0].id,
        "description": cup_sizes_on_db[0].description,
        "amount_ml": cup_sizes_on_db[0].amount_ml,
    }
