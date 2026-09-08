# Signup Flow Proof

This extension shows the same core capability as FraudFlow from a **Tech Analyst / digital onboarding** perspective rather than a pure fraud-operations perspective.

The data is synthetic. It does not reproduce or claim knowledge of any bank's production architecture.

## User story

**As an onboarding team, we need account-opening side effects to happen only after customer data, identity and KYC gates are satisfied, while retries, duplicate events and manual review remain traceable.**

## Flow

`Signup -> data validation -> identity -> KYC -> account-open gate`

## Requirement to evidence

| Requirement | Technical behaviour | Automated evidence |
|---|---|---|
| Do not open an account before all prerequisites pass | Side-effect gate checks validated data + verified identity + cleared KYC | `test_happy_path_and_side_effect_gate` |
| Identity mismatch needs human review | Mismatch sets `MANUAL_REVIEW`; account-open request is blocked | `test_identity_mismatch_blocks_account_opening` |
| Provider timeout must be safely retryable | Timeout creates a retryable state without an account-opening side effect | `test_provider_timeout_is_retryable_and_safe` |
| Duplicate / out-of-order events must stay safe | Duplicate event IDs are ignored; premature account-open requests remain blocked | `test_duplicate_and_out_of_order_events_stay_safe` |

## Why this is a Tech Analyst proof

The point is not the toy onboarding domain itself. The point is the translation chain:

**requirement -> data/event contract -> state transition -> side-effect boundary -> acceptance criterion -> executable test**

That is the work I want a reviewer to inspect.

## Integration decision: sync vs async

**Synchronous** calls are useful when the customer is waiting for an immediate validation response and the result is required to continue the current UI step.

**Asynchronous events** are useful for durable downstream state changes, retries, auditability and decoupled integrations across services.

In a production system the exact choice depends on latency requirements, ownership boundaries, delivery guarantees, failure modes and observability. This proof intentionally models the boundary rather than pretending there is one universal answer.

## Deliberate constraints

- synthetic data only
- no copied banking UI or internal architecture
- no real KYC/AML decision engine
- no claim that the reducer is production-complete
- no automatic bypass of human review
