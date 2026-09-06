from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_route():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_investigator_cockpit_route():
    response = client.get("/")
    assert response.status_code == 200
    assert "FraudFlow" in response.text
    assert "Inject card-testing scenario" in response.text
