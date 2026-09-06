import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.models import AnalystDecision, Decision, TransactionEvent
from app.seed import card_testing_events
from app.service import FraudService


def card_testing_eval():
    service = FraudService()
    case = None
    for event in card_testing_events():
        case = service.ingest(event) or case
    names = {s.name for s in case.signals} if case else set()
    passed = bool(
        case
        and case.risk_score >= 60
        and {"transaction_velocity", "amount_anomaly"} <= names
        and all(s.evidence for s in case.signals)
    )
    return (
        passed,
        {
            "case_created": bool(case),
            "risk_score": case.risk_score if case else None,
            "signals": sorted(names),
        },
        service,
        case,
    )


def routine_customer_eval():
    service = FraudService()
    base = datetime(2026, 9, 6, 8, 0, tzinfo=timezone.utc)
    cases = []
    for i, amount in enumerate([18.0, 20.0, 17.0]):
        event = TransactionEvent(
            event_id=f"normal_evt_{i}",
            customer_id="cust_normal",
            account_id="acct_normal",
            transaction_id=f"normal_txn_{i}",
            timestamp=base + timedelta(minutes=i * 10),
            amount_eur=amount,
            city="Berlin",
            country="DE",
            device_id="device_known",
            ip_address="198.51.100.8",
            merchant="Synthetic Grocery",
            authorized=True,
        )
        maybe = service.ingest(event)
        if maybe:
            cases.append(maybe.case_id)
    return len(cases) == 0, {"cases_created": cases}


def impossible_travel_eval():
    service = FraudService()
    base = datetime(2026, 9, 6, 9, 0, tzinfo=timezone.utc)
    first = TransactionEvent(
        event_id="travel_evt_1",
        customer_id="cust_travel",
        account_id="acct_travel",
        transaction_id="travel_txn_1",
        timestamp=base,
        amount_eur=40,
        city="Berlin",
        country="DE",
        device_id="device_known",
        ip_address="198.51.100.10",
        merchant="Synthetic Cafe",
        authorized=True,
    )
    second = TransactionEvent(
        event_id="travel_evt_2",
        customer_id="cust_travel",
        account_id="acct_travel",
        transaction_id="travel_txn_2",
        timestamp=base + timedelta(minutes=30),
        amount_eur=45,
        city="Singapore",
        country="SG",
        device_id="device_new",
        ip_address="203.0.113.90",
        merchant="Synthetic Merchant SG",
        authorized=True,
    )
    service.ingest(first)
    case = service.ingest(second)
    names = {s.name for s in case.signals} if case else set()
    passed = bool(
        case
        and case.risk_score >= 70
        and {"new_device", "impossible_travel"} <= names
    )
    return passed, {
        "case_created": bool(case),
        "risk_score": case.risk_score if case else None,
        "signals": sorted(names),
    }


def human_decision_eval(service, case):
    if not case:
        return False, {"reason": "no case available"}
    service.decide(
        case.case_id,
        AnalystDecision(
            decision=Decision.BLOCK,
            analyst="eval-analyst",
            reason="Evidence reviewed in golden scenario",
        ),
    )
    audit = service.get_audit(case.case_id)
    last = audit[-1]
    passed = (
        last.action == "ANALYST_DECISION"
        and last.details.get("decision") == "BLOCK"
        and bool(last.details.get("evidence_visible"))
    )
    return passed, {
        "audit_entries": len(audit),
        "last_action": last.action,
        "decision": last.details.get("decision"),
        "evidence_visible": bool(last.details.get("evidence_visible")),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check", action="store_true", help="exit non-zero if any eval fails"
    )
    args = parser.parse_args()

    e1, d1, service, case = card_testing_eval()
    e2, d2 = routine_customer_eval()
    e3, d3 = impossible_travel_eval()
    e4, d4 = human_decision_eval(service, case)

    results = {
        "suite": "fraudflow-behavioural-evals-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "passed": all([e1, e2, e3, e4]),
        "results": {
            "card_testing_escalation": {"passed": e1, **d1},
            "routine_customer_no_alert": {"passed": e2, **d2},
            "impossible_travel_takeover": {"passed": e3, **d3},
            "human_decision_audit": {"passed": e4, **d4},
        },
    }
    Path("evidence").mkdir(exist_ok=True)
    Path("evidence/eval-results.json").write_text(
        json.dumps(results, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(results, indent=2))
    if args.check and not results["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
