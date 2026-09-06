from app.models import AnalystDecision, Decision
from app.seed import card_testing_events
from app.service import FraudService


def test_card_testing_golden_case_creates_evidence_backed_case():
    service = FraudService()
    case = None

    for event in card_testing_events():
        maybe_case = service.ingest(event)
        if maybe_case:
            case = maybe_case

    assert case is not None
    assert case.risk_score >= 50
    assert case.recommended_decision in {Decision.REVIEW, Decision.BLOCK}
    assert len(case.signals) >= 2
    assert all(signal.evidence for signal in case.signals)

    signal_names = {signal.name for signal in case.signals}
    assert "transaction_velocity" in signal_names
    assert "amount_anomaly" in signal_names

    service.decide(
        case.case_id,
        AnalystDecision(
            decision=Decision.BLOCK,
            analyst="test-analyst",
            reason="Card-testing sequence followed by high-value transaction",
        ),
    )

    audit = service.get_audit(case.case_id)
    assert audit[-1].action == "ANALYST_DECISION"
    assert audit[-1].details["decision"] == "BLOCK"
    assert audit[-1].details["evidence_visible"]
