# DKB Requirement Map

This document maps the FraudFlow proof to the capabilities expected in a junior fraud data / technology analyst role.

| Role capability | FraudFlow evidence | Notes |
|---|---|---|
| Understand fraud processes | Card-testing golden scenario and case lifecycle | Synthetic and intentionally narrow |
| Analyse data flows and data models | TransactionEvent, FraudCase, Signal and AuditEntry models | Explicit schemas rather than implicit dictionaries |
| Translate domain needs into engineering requirements | Event → signal → decision → review → audit architecture | README documents the operational contract |
| REST/API understanding | FastAPI endpoints for events, cases, decisions and audit | Runnable locally |
| Event-stream thinking | Event-oriented ingestion boundary | Kafka is not claimed as implemented |
| Data quality / trustworthy signals | Deterministic evidence-bearing signals | Every signal carries source evidence |
| Human review workflows | ALLOW / REVIEW / BLOCK decision model | Analyst action is persisted in the audit trail |
| Fraud detection logic | Velocity, new device, amount anomaly, impossible travel | Demonstration rules, not production detection logic |
| Git / software delivery | Public repository with runnable service and tests | Small by design |
| Python | FastAPI / Pydantic implementation | Direct evidence |
| Communication between domain and technology | README, architecture and requirement mapping | Designed for hiring-manager review |

## What is deliberately not claimed

FraudFlow does **not** claim:

- production banking experience,
- production Kafka operation,
- trained fraud ML models,
- access to bank data,
- regulatory certification,
- or production-grade fraud thresholds.

The proof demonstrates how I reason about fraud-data integration and analyst workflows using transparent synthetic data.

## 90-second review path

1. Read the architecture in the README.
2. Run `POST /demo/card-testing`.
3. Inspect the returned signals and their evidence.
4. Open the generated case.
5. Submit a human `BLOCK` decision.
6. Fetch the audit trail and verify the decision and visible evidence were persisted.

## Interview discussion prompts

The proof is also intended to open useful technical discussion:

- Where should rule evaluation live in the real fraud platform?
- Which events are authoritative versus derived?
- How are event ordering and duplicate delivery handled?
- How are thresholds versioned and approved?
- Which signals should block synchronously versus create asynchronous review cases?
- How is analyst feedback returned to rule/model development?
- What should be monitored for drift, data loss and sudden false-positive changes?

These are intentionally left as architecture questions rather than hidden behind fake implementation complexity.
