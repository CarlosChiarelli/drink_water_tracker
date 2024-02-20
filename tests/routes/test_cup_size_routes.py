from fastapi import status
from fastapi.testclient import TestClient

from drink_water_tracker.db.models import CupSize as CupSizeModel
from drink_water_tracker.main import app

client = TestClient(app)


def test_add_cup_size_route(db_session):
    body = {"description": "Copo médio 350mL", "amount_ml": 350}
    response = client.post("/cup-size/add", json=body)
    assert response.status_code == status.HTTP_201_CREATED

    cup_size_on_db = db_session.query(CupSizeModel).all()
    assert len(cup_size_on_db) == 1

    db_session.delete(cup_size_on_db[0])
    db_session.commit()


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
