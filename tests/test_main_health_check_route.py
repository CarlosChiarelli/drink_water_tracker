from fastapi import status
from fastapi.testclient import TestClient

from drink_water_tracker.main import app

client = TestClient(app)


def test_main_health_check_route(db_session):
    response = client.get("/health-check")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() is True
