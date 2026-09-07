CAPABILITY_MAP = [
    {
        "requirement": "Fraud Data & Analytics",
        "proof": "Zahlungen werden als strukturierte Events verarbeitet und in nachvollziehbare Signale, Fälle und Entscheidungen übersetzt.",
        "url": "https://github.com/mikelninh/fraudflow-dkb/blob/main/.ai-build/ARCHITECTURE.md",
    },
    {
        "requirement": "Fraud Prevention & Controls",
        "proof": "Auffällige Muster erzeugen einen erklärbaren Prüffall; Normalverhalten wird als Negativfall getestet und ein Mensch behält die finale Entscheidung.",
        "url": "https://github.com/mikelninh/fraudflow-dkb/blob/main/.ai-build/EVALS.md",
    },
    {
        "requirement": "Platform & Integration",
        "proof": "Typed domain models, FastAPI-Grenzen und event-orientierte Schnittstellen zeigen die Übersetzung von Fraud-Anforderungen in technische Verträge.",
        "url": "https://github.com/mikelninh/fraudflow-dkb/blob/main/app/main.py",
    },
    {
        "requirement": "Governance & Auditability",
        "proof": "Signalgründe, menschliche Entscheidungen, Audit-Trail, Acceptance Criteria und reproduzierbare Evidence bleiben prüfbar.",
        "url": "https://github.com/mikelninh/fraudflow-dkb/blob/main/evidence/PROOF_INDEX.md",
    },
    {
        "requirement": "Communication & Product Thinking",
        "proof": "Die Hauptjourney erklärt denselben technischen Vorgang zuerst in Alltagssprache; Engineer-Details bleiben bei Bedarf zugänglich.",
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
    return {
        "passed": passed,
        "total": len(evaluations),
        "evals": evaluations,
        "capability_map": CAPABILITY_MAP,
    }
