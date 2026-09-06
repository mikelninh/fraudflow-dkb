ROLE_MAP = [
    {
        "requirement": "Fachliche Anforderungen in ein technisches System übersetzen",
        "proof": "Explizite Anforderungen und Acceptance Criteria plus klar getrennte Event-, Case- und API-Modelle.",
        "url": "https://github.com/mikelninh/fraudflow-dkb/blob/main/.ai-build/SPEC.md",
    },
    {
        "requirement": "Datenflüsse und Abhängigkeiten nachvollziehen",
        "proof": "Zahlung → auffälliges Muster → Fraud Case → menschliche Entscheidung → Audit-Trail.",
        "url": "https://github.com/mikelninh/fraudflow-dkb/blob/main/.ai-build/ARCHITECTURE.md",
    },
    {
        "requirement": "Mit APIs und event-getriebenen Systemen arbeiten",
        "proof": "Event-basierte REST-Schnittstelle; Kafka-kompatible Systemgrenze ohne behauptete Production-Kafka-Erfahrung.",
        "url": "https://github.com/mikelninh/fraudflow-dkb/blob/main/app/main.py",
    },
    {
        "requirement": "Umsetzung mit Tests und klaren Abnahmekriterien begleiten",
        "proof": "Golden Case, Negativfall, adversarialer Fall, Behavioural Evals und CI-Gate.",
        "url": "https://github.com/mikelninh/fraudflow-dkb/blob/main/.ai-build/EVALS.md",
    },
    {
        "requirement": "Komplexe technische Themen verständlich kommunizieren",
        "proof": "Einfache Reviewer-Journey für HR/Hiring Manager; technische Details bleiben für Engineers prüfbar.",
        "url": "https://github.com/mikelninh/fraudflow-dkb/blob/main/docs/UX_PRINCIPLES.md",
    },
]

EVAL_LABELS = {
    "card_testing_escalation": "Auffälliges Kartenmuster wird erkannt",
    "routine_customer_no_alert": "Normales Verhalten löst keinen falschen Alarm aus",
    "impossible_travel_takeover": "Neues Gerät + unmöglicher Standortwechsel werden erkannt",
    "human_decision_audit": "Menschliche Entscheidung bleibt nachvollziehbar",
}


def proof_summary(results: dict) -> dict:
    evaluations = []
    for key, value in results.get("results", {}).items():
        if key == "card_testing_escalation":
            detail = "5 Zahlungen in kurzer Folge; Fall wird mit nachvollziehbaren Gründen eröffnet"
        elif key == "routine_customer_no_alert":
            detail = "0 Fälle bei normaler synthetischer Nutzung"
        elif key == "impossible_travel_takeover":
            detail = "neues Gerät + schneller Länderwechsel erzeugen einen Prüffall"
        else:
            detail = "Entscheidung und sichtbare Evidenz werden im Audit-Trail gespeichert"
        evaluations.append({
            "key": key,
            "label": EVAL_LABELS.get(key, key.replace("_", " ").title()),
            "passed": bool(value.get("passed")),
            "detail": detail,
        })
    passed = sum(1 for item in evaluations if item["passed"])
    return {"passed": passed, "total": len(evaluations), "evals": evaluations, "role_map": ROLE_MAP}
