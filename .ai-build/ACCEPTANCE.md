# ACCEPTANCE

FraudFlow is release-ready only when all critical criteria pass.

## Product
- [x] Root route serves the investigator cockpit.
- [x] Synthetic card-testing scenario is runnable from the UI/API.
- [x] A suspicious event can create a persisted fraud case.
- [x] Every surfaced signal contains inspectable evidence.
- [x] Human ALLOW / REVIEW / BLOCK decisions are recorded in the audit trail.

## Behavioural proof
- [x] Golden card-testing scenario creates a case with risk score >= 60.
- [x] Golden card-testing scenario includes `transaction_velocity` and `amount_anomaly`.
- [x] Routine customer activity produces no fraud case.
- [x] Rapid country change plus unseen device produces `impossible_travel` and `new_device` and creates a case.
- [x] Analyst decision creates an `ANALYST_DECISION` audit entry with visible evidence.

## Engineering
- [x] Tests exist for the golden path.
- [x] Behavioural eval runner covers positive and negative cases.
- [x] CI checks repository contract, tests and evals.
- [x] Build OS files are present and non-empty.
- [ ] Production deployment is healthy and manually smoke-tested.

## Release command

```bash
python scripts/check_build_os.py && pytest -q && python evals/run_evals.py --check
```
