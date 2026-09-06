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


def test_card_testing_demo_is_repeatable():
    first = client.post("/demo/card-testing")
    second = client.post("/demo/card-testing")

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["risk_score"] == 65
    assert second.json()["risk_score"] == 65
    assert {signal["name"] for signal in first.json()["signals"]} == {
        "transaction_velocity",
        "amount_anomaly",
    }
    assert {signal["name"] for signal in second.json()["signals"]} == {
        "transaction_velocity",
        "amount_anomaly",
    }
