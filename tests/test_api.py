from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_route():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_investigator_cockpit_route():
    response = client.get("/")
    assert response.status_code == 200
    assert "FraudFlow" in response.text
    assert "Fraud Operations & Decision Systems" in response.text
    assert "90-Sekunden-Fall starten" in response.text
    assert "Warum sollte jemand hinschauen?" in response.text
    assert "Kein Fraud-Vorwissen nötig" in response.text
    assert "Wo diese Arbeit einsetzbar ist" in response.text
    assert "DKB Arbeitsprobe" not in response.text
    assert "N26" not in response.text


def test_frontend_assets_are_served():
    response = client.get("/ui/styles.css")
    assert response.status_code == 200
    assert "--blue:#148dea" in response.text


def test_proof_summary_exposes_reproducible_eval_results():
    response = client.get("/proof/summary")
    assert response.status_code == 200
    payload = response.json()
    assert payload["passed"] == payload["total"] == 4
    assert len(payload["capability_map"]) >= 5
    assert "role_map" not in payload
    assert any("Normales Verhalten" in item["label"] for item in payload["evals"])
    assert any(item["requirement"] == "Fraud Prevention & Controls" for item in payload["capability_map"])


def test_card_testing_demo_is_repeatable_and_source_traceable():
    first = client.post("/demo/card-testing")
    second = client.post("/demo/card-testing")

    assert first.status_code == 200
    assert second.status_code == 200
    for response in (first, second):
        payload = response.json()
        assert len(payload["source_events"]) == 5
        assert payload["case"]["risk_score"] == 65
        assert {signal["name"] for signal in payload["case"]["signals"]} == {
            "transaction_velocity",
            "amount_anomaly",
        }
