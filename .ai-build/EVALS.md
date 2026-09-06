# EVALS

## Purpose
Test behaviour, not just code paths. The eval suite asks whether FraudFlow distinguishes deliberately suspicious patterns from routine synthetic activity and preserves evidence through review.

## Golden cases

### E1 — Card testing → escalation
Five transactions in 27 seconds: four low-value attempts followed by €499.

Pass:
- case created
- risk >= 60
- `transaction_velocity` present
- `amount_anomaly` present
- evidence non-empty

### E2 — Routine customer
Three ordinary-value events from the same device/country, separated by more than the velocity window.

Pass:
- no case created

### E3 — Account takeover / impossible travel
Known Berlin device followed 30 minutes later by a new device in Singapore.

Pass:
- case created
- risk >= 70
- `new_device` present
- `impossible_travel` present

### E4 — Human decision trace
Close a surfaced case after evidence review.

Pass:
- final audit event is `ANALYST_DECISION`
- decision and visible evidence are retained

## Release threshold
All four evals must pass. There is no partial-credit production gate for this work sample.

## Command
`python evals/run_evals.py --check`
