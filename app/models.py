from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Decision(str, Enum):
    ALLOW = "ALLOW"
    REVIEW = "REVIEW"
    BLOCK = "BLOCK"


class TransactionEvent(BaseModel):
    event_id: str
    customer_id: str
    account_id: str
    transaction_id: str
    timestamp: datetime
    amount_eur: float = Field(gt=0)
    city: str
    country: str
    device_id: str
    ip_address: str
    merchant: str
    authorized: bool = True


class Signal(BaseModel):
    name: str
    score: int = Field(ge=0, le=100)
    confidence: str
    evidence: dict[str, Any]


class FraudCase(BaseModel):
    case_id: str
    customer_id: str
    account_id: str
    transaction_id: str
    created_at: datetime
    risk_score: int
    recommended_decision: Decision
    signals: list[Signal]
    related_event_ids: list[str]
    status: str = "OPEN"


class AnalystDecision(BaseModel):
    decision: Decision
    analyst: str
    reason: str


class AuditEntry(BaseModel):
    timestamp: datetime
    action: str
    actor: str
    details: dict[str, Any]
