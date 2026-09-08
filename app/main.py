import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .models import AnalystDecision, FraudCase, TransactionEvent
from .proof import proof_summary
from .seed import card_testing_events
from .service import service
from .signup_flow import signup_demo_scenarios

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"
EVIDENCE = ROOT / "evidence" / "eval-results.json"

app = FastAPI(
    title="FraudFlow",
    description="Synthetic fraud data, decision systems and signup-flow proof-of-work",
    version="0.5.0",
)
app.mount("/ui", StaticFiles(directory=FRONTEND), name="ui")


@app.get("/", include_in_schema=False)
def investigator_cockpit():
    return FileResponse(FRONTEND / "index.html")


@app.get("/signup", include_in_schema=False)
def signup_flow_cockpit():
    return FileResponse(FRONTEND / "signup.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": "0.5.0"}


@app.post("/events/transaction", response_model=FraudCase | None)
def ingest_transaction(event: TransactionEvent) -> FraudCase | None:
    return service.ingest(event)


@app.get("/cases/{case_id}", response_model=FraudCase)
def get_case(case_id: str) -> FraudCase:
    try:
        return service.get_case(case_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Case not found") from exc


@app.post("/cases/{case_id}/decision", response_model=FraudCase)
def decide_case(case_id: str, decision: AnalystDecision) -> FraudCase:
    try:
        return service.decide(case_id, decision)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Case not found") from exc


@app.get("/cases/{case_id}/audit")
def get_case_audit(case_id: str):
    try:
        return service.get_audit(case_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Case not found") from exc


@app.get("/proof/summary")
def get_proof_summary():
    try:
        results = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=503, detail="Proof evidence unavailable") from exc
    return proof_summary(results)


@app.post("/demo/card-testing")
def run_card_testing_demo():
    service.reset()
    events = card_testing_events()
    created_case = None
    for event in events:
        maybe_case = service.ingest(event)
        if maybe_case:
            created_case = maybe_case
    if not created_case:
        raise HTTPException(status_code=500, detail="Golden scenario did not create a case")
    return {
        "source_events": [event.model_dump(mode="json") for event in events],
        "case": created_case.model_dump(mode="json"),
    }


@app.get("/demo/signup-flow")
def run_signup_flow_demo():
    return signup_demo_scenarios()
