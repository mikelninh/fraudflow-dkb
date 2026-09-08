from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class SignupEventType(str, Enum):
    SIGNUP_STARTED = "SIGNUP_STARTED"
    CUSTOMER_DATA_VALIDATED = "CUSTOMER_DATA_VALIDATED"
    IDENTITY_VERIFIED = "IDENTITY_VERIFIED"
    IDENTITY_MISMATCH = "IDENTITY_MISMATCH"
    IDENTITY_PROVIDER_TIMEOUT = "IDENTITY_PROVIDER_TIMEOUT"
    KYC_CLEARED = "KYC_CLEARED"
    KYC_REVIEW = "KYC_REVIEW"
    ACCOUNT_OPEN_REQUESTED = "ACCOUNT_OPEN_REQUESTED"


class SignupEvent(BaseModel):
    event_id: str
    correlation_id: str
    occurred_at: datetime
    event_type: SignupEventType
    source: str
    payload: dict[str, Any] = Field(default_factory=dict)


class FlowAudit(BaseModel):
    event_id: str
    action: str
    detail: str


class SignupFlowResult(BaseModel):
    correlation_id: str
    outcome: str
    next_step: str
    data_validated: bool
    identity_status: str
    kyc_status: str
    account_status: str
    retry_required: bool
    manual_review: bool
    processed_event_ids: list[str]
    audit: list[FlowAudit]


def evaluate_signup(events: list[SignupEvent]) -> SignupFlowResult:
    """Deterministic signup-flow reducer with idempotency and safe side-effect gates."""
    if not events:
        raise ValueError("At least one signup event is required")

    correlation_id = events[0].correlation_id
    data_validated = False
    identity_status = "PENDING"
    kyc_status = "PENDING"
    account_status = "NOT_OPENED"
    retry_required = False
    manual_review = False
    seen: set[str] = set()
    processed: list[str] = []
    audit: list[FlowAudit] = []

    for event in events:
        if event.correlation_id != correlation_id:
            audit.append(FlowAudit(event_id=event.event_id, action="REJECTED", detail="correlation_id mismatch"))
            continue
        if event.event_id in seen:
            audit.append(FlowAudit(event_id=event.event_id, action="IGNORED_DUPLICATE", detail="idempotency key already processed"))
            continue

        seen.add(event.event_id)
        processed.append(event.event_id)

        if event.event_type == SignupEventType.SIGNUP_STARTED:
            audit.append(FlowAudit(event_id=event.event_id, action="ACCEPTED", detail="signup context created"))

        elif event.event_type == SignupEventType.CUSTOMER_DATA_VALIDATED:
            valid = bool(event.payload.get("valid", False))
            data_validated = valid
            if valid:
                audit.append(FlowAudit(event_id=event.event_id, action="ACCEPTED", detail="required customer data validated"))
            else:
                manual_review = True
                audit.append(FlowAudit(event_id=event.event_id, action="REVIEW_REQUIRED", detail="customer data incomplete or inconsistent"))

        elif event.event_type == SignupEventType.IDENTITY_VERIFIED:
            identity_status = "VERIFIED"
            retry_required = False
            audit.append(FlowAudit(event_id=event.event_id, action="ACCEPTED", detail="identity provider returned verified"))

        elif event.event_type == SignupEventType.IDENTITY_MISMATCH:
            identity_status = "MISMATCH"
            manual_review = True
            audit.append(FlowAudit(event_id=event.event_id, action="REVIEW_REQUIRED", detail="identity result conflicts with signup data"))

        elif event.event_type == SignupEventType.IDENTITY_PROVIDER_TIMEOUT:
            identity_status = "RETRYABLE_ERROR"
            retry_required = True
            audit.append(FlowAudit(event_id=event.event_id, action="RETRY_REQUIRED", detail="provider timeout recorded without opening account"))

        elif event.event_type == SignupEventType.KYC_CLEARED:
            kyc_status = "CLEARED"
            audit.append(FlowAudit(event_id=event.event_id, action="ACCEPTED", detail="KYC gate cleared"))

        elif event.event_type == SignupEventType.KYC_REVIEW:
            kyc_status = "REVIEW"
            manual_review = True
            audit.append(FlowAudit(event_id=event.event_id, action="REVIEW_REQUIRED", detail="KYC requires human review"))

        elif event.event_type == SignupEventType.ACCOUNT_OPEN_REQUESTED:
            prerequisites_ok = data_validated and identity_status == "VERIFIED" and kyc_status == "CLEARED"
            if prerequisites_ok and not manual_review:
                account_status = "OPENED"
                audit.append(FlowAudit(event_id=event.event_id, action="SIDE_EFFECT_ALLOWED", detail="all signup gates passed"))
            else:
                audit.append(FlowAudit(event_id=event.event_id, action="SIDE_EFFECT_BLOCKED", detail="account opening blocked until all gates pass"))

    if account_status == "OPENED":
        outcome = "COMPLETED"
        next_step = "Signup complete"
    elif manual_review:
        outcome = "MANUAL_REVIEW"
        next_step = "Review identity/KYC evidence before any account-opening side effect"
    elif retry_required:
        outcome = "RETRY_IDENTITY_PROVIDER"
        next_step = "Retry the identity provider with the same correlation context"
    elif data_validated and identity_status == "VERIFIED" and kyc_status == "CLEARED":
        outcome = "READY_TO_OPEN"
        next_step = "Issue a fresh account-open request; earlier blocked requests stay blocked"
    else:
        outcome = "IN_PROGRESS"
        next_step = "Wait for the next required signup event"

    return SignupFlowResult(
        correlation_id=correlation_id,
        outcome=outcome,
        next_step=next_step,
        data_validated=data_validated,
        identity_status=identity_status,
        kyc_status=kyc_status,
        account_status=account_status,
        retry_required=retry_required,
        manual_review=manual_review,
        processed_event_ids=processed,
        audit=audit,
    )


def _event(event_id: str, event_type: SignupEventType, seconds: int, payload: dict[str, Any] | None = None) -> SignupEvent:
    return SignupEvent(
        event_id=event_id,
        correlation_id="signup_demo_001",
        occurred_at=datetime(2026, 9, 8, 10, 0, seconds, tzinfo=timezone.utc),
        event_type=event_type,
        source={
            SignupEventType.SIGNUP_STARTED: "signup-web",
            SignupEventType.CUSTOMER_DATA_VALIDATED: "validation-service",
            SignupEventType.IDENTITY_VERIFIED: "identity-provider",
            SignupEventType.IDENTITY_MISMATCH: "identity-provider",
            SignupEventType.IDENTITY_PROVIDER_TIMEOUT: "identity-adapter",
            SignupEventType.KYC_CLEARED: "compliance-service",
            SignupEventType.KYC_REVIEW: "compliance-service",
            SignupEventType.ACCOUNT_OPEN_REQUESTED: "account-orchestrator",
        }[event_type],
        payload=payload or {},
    )


def signup_demo_scenarios() -> dict[str, Any]:
    scenarios: dict[str, list[SignupEvent]] = {
        "happy_path": [
            _event("s1", SignupEventType.SIGNUP_STARTED, 0),
            _event("s2", SignupEventType.CUSTOMER_DATA_VALIDATED, 2, {"valid": True}),
            _event("s3", SignupEventType.IDENTITY_VERIFIED, 4),
            _event("s4", SignupEventType.KYC_CLEARED, 6),
            _event("s5", SignupEventType.ACCOUNT_OPEN_REQUESTED, 8),
        ],
        "identity_mismatch": [
            _event("m1", SignupEventType.SIGNUP_STARTED, 0),
            _event("m2", SignupEventType.CUSTOMER_DATA_VALIDATED, 2, {"valid": True}),
            _event("m3", SignupEventType.IDENTITY_MISMATCH, 4),
            _event("m4", SignupEventType.ACCOUNT_OPEN_REQUESTED, 6),
        ],
        "provider_timeout": [
            _event("t1", SignupEventType.SIGNUP_STARTED, 0),
            _event("t2", SignupEventType.CUSTOMER_DATA_VALIDATED, 2, {"valid": True}),
            _event("t3", SignupEventType.IDENTITY_PROVIDER_TIMEOUT, 4),
            _event("t4", SignupEventType.ACCOUNT_OPEN_REQUESTED, 6),
        ],
        "duplicate_out_of_order": [
            _event("o1", SignupEventType.SIGNUP_STARTED, 0),
            _event("o5", SignupEventType.ACCOUNT_OPEN_REQUESTED, 1),
            _event("o2", SignupEventType.CUSTOMER_DATA_VALIDATED, 2, {"valid": True}),
            _event("o3", SignupEventType.IDENTITY_VERIFIED, 4),
            _event("o3", SignupEventType.IDENTITY_VERIFIED, 4),
            _event("o4", SignupEventType.KYC_CLEARED, 6),
        ],
    }

    labels = {
        "happy_path": "Happy path",
        "identity_mismatch": "Identity mismatch",
        "provider_timeout": "Provider timeout",
        "duplicate_out_of_order": "Duplicate + out-of-order event",
    }
    results: dict[str, dict[str, Any]] = {}
    for key, events in scenarios.items():
        results[key] = {
            "label": labels[key],
            "events": [event.model_dump(mode="json") for event in events],
            "result": evaluate_signup(events).model_dump(mode="json"),
        }

    return {
        "flow": ["Signup", "Data validation", "Identity", "KYC", "Account-open gate"],
        "scenarios": results,
        "requirement_trace": [
            {"requirement": "No account opening before data, identity and KYC gates pass", "test": "test_happy_path_and_side_effect_gate"},
            {"requirement": "Identity mismatch routes to human review", "test": "test_identity_mismatch_blocks_account_opening"},
            {"requirement": "Provider timeouts are retryable without unsafe side effects", "test": "test_provider_timeout_is_retryable_and_safe"},
            {"requirement": "Duplicate and out-of-order events are handled idempotently", "test": "test_duplicate_and_out_of_order_events_stay_safe"},
        ],
        "integration_decision": {
            "sync": "Use synchronous calls for immediate validation when the user is waiting for a response.",
            "async": "Use events for durable downstream state changes, retries and auditability across services.",
        },
    }
