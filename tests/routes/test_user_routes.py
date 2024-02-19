from fastapi import status
from fastapi.testclient import TestClient

from drink_water_tracker.db.models import User as UserModel
from drink_water_tracker.main import app

client = TestClient(app)


def test_add_user_route(db_session):
    body = {"name": "Carlos", "weight": 70}
    response = client.post("/user/add", json=body)
    assert response.status_code == status.HTTP_201_CREATED

    users_on_db = db_session.query(UserModel).all()
    assert len(users_on_db) == 1

    db_session.delete(users_on_db[0])
    db_session.commit()
