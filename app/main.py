from fastapi import FastAPI, HTTPException

from .models import AnalystDecision, FraudCase, TransactionEvent
from .seed import card_testing_events
from .service import service

app = FastAPI(
    title="FraudFlow",
    description="Synthetic fraud data & integration proof-of-work",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


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


@app.post("/demo/card-testing")
def run_card_testing_demo():
    created_case = None
    for event in card_testing_events():
        maybe_case = service.ingest(event)
        if maybe_case:
            created_case = maybe_case
    if not created_case:
        raise HTTPException(status_code=500, detail="Golden scenario did not create a case")
    return created_case
