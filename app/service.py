from datetime import datetime, timezone
from uuid import uuid4

from .models import AnalystDecision, AuditEntry, Decision, FraudCase, TransactionEvent
from .rules import detect_signals, risk_score


class FraudService:
    def __init__(self) -> None:
        self.events: list[TransactionEvent] = []
        self.cases: dict[str, FraudCase] = {}
        self.audit: dict[str, list[AuditEntry]] = {}

    def ingest(self, event: TransactionEvent) -> FraudCase | None:
        history = [e for e in self.events if e.customer_id == event.customer_id]
        signals = detect_signals(event, history)
        self.events.append(event)

        score = risk_score(signals)
        if score < 50:
            return None

        decision = Decision.BLOCK if score >= 85 else Decision.REVIEW
        case_id = f"case_{uuid4().hex[:10]}"
        case = FraudCase(
            case_id=case_id,
            customer_id=event.customer_id,
            account_id=event.account_id,
            transaction_id=event.transaction_id,
            created_at=datetime.now(timezone.utc),
            risk_score=score,
            recommended_decision=decision,
            signals=signals,
            related_event_ids=[e.event_id for e in history[-10:]] + [event.event_id],
        )
        self.cases[case_id] = case
        self.audit[case_id] = [
            AuditEntry(
                timestamp=datetime.now(timezone.utc),
                action="CASE_CREATED",
                actor="fraudflow",
                details={
                    "risk_score": score,
                    "recommended_decision": decision.value,
                    "signals": [signal.name for signal in signals],
                },
            )
        ]
        return case

    def get_case(self, case_id: str) -> FraudCase:
        return self.cases[case_id]

    def decide(self, case_id: str, decision: AnalystDecision) -> FraudCase:
        case = self.cases[case_id]
        case.status = "CLOSED"
        self.audit[case_id].append(
            AuditEntry(
                timestamp=datetime.now(timezone.utc),
                action="ANALYST_DECISION",
                actor=decision.analyst,
                details={
                    "decision": decision.decision.value,
                    "reason": decision.reason,
                    "evidence_visible": [signal.model_dump() for signal in case.signals],
                },
            )
        )
        return case

    def get_audit(self, case_id: str) -> list[AuditEntry]:
        return self.audit[case_id]


service = FraudService()
