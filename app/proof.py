ROLE_MAP = [
    {
        "requirement": "Translate business requirements into implementable technical requirements",
        "proof": "Explicit SPEC + ACCEPTANCE contracts, typed event/case models and a small REST boundary.",
        "url": "https://github.com/mikelninh/fraudflow-dkb/blob/main/.ai-build/SPEC.md",
    },
    {
        "requirement": "Analyse data structures, models and cross-system data flows",
        "proof": "TransactionEvent → deterministic signal engine → FraudCase → human decision → AuditEntry.",
        "url": "https://github.com/mikelninh/fraudflow-dkb/blob/main/.ai-build/ARCHITECTURE.md",
    },
    {
        "requirement": "Work with REST APIs and event-driven architectures",
        "proof": "Event-shaped ingestion API and documented boundary that is Kafka-compatible without claiming production Kafka experience.",
        "url": "https://github.com/mikelninh/fraudflow-dkb/blob/main/app/main.py",
    },
    {
        "requirement": "Accompany implementation from requirements through testing",
        "proof": "Golden, negative and adversarial behavioural evals plus CI gates and a release runbook.",
        "url": "https://github.com/mikelninh/fraudflow-dkb/blob/main/.ai-build/EVALS.md",
    },
    {
        "requirement": "Communicate complex technical topics clearly",
        "proof": "Hiring-manager-first cockpit plus explicit USERS.md for HR, fraud lead and engineer review paths.",
        "url": "https://github.com/mikelninh/fraudflow-dkb/blob/main/.ai-build/USERS.md",
    },
]

EVAL_LABELS = {
    "card_testing_escalation": "Card testing → escalation",
    "routine_customer_no_alert": "Routine customer → no false alert",
    "impossible_travel_takeover": "Impossible travel + new device",
    "human_decision_audit": "Human decision → audit evidence",
}


def proof_summary(results: dict) -> dict:
    evaluations = []
    for key, value in results.get("results", {}).items():
        if key == "card_testing_escalation":
            detail = f"risk {value.get('risk_score')} · {', '.join(value.get('signals', []))}"
        elif key == "routine_customer_no_alert":
            detail = "0 cases created for routine synthetic activity"
        elif key == "impossible_travel_takeover":
            detail = f"risk {value.get('risk_score')} · {', '.join(value.get('signals', []))}"
        else:
            detail = f"{value.get('last_action')} · evidence retained: {value.get('evidence_visible')}"
        evaluations.append({
            "key": key,
            "label": EVAL_LABELS.get(key, key.replace("_", " ").title()),
            "passed": bool(value.get("passed")),
            "detail": detail,
        })
    passed = sum(1 for item in evaluations if item["passed"])
    return {"passed": passed, "total": len(evaluations), "evals": evaluations, "role_map": ROLE_MAP}
