# ACCEPTANCE

FraudFlow is release-ready only when all critical criteria pass.

## User experience
- [x] Explicit users are documented in `.ai-build/USERS.md`.
- [x] Root route explains role relevance before asking the reviewer to interact.
- [x] There is one obvious primary CTA: `Start 90-second investigation`.
- [x] The UI guides the reviewer through Source → Interpretation → Decision → Proof.
- [x] Raw source events are visible, including event IDs and values.
- [x] Signal evidence is visible next to each triggered signal.
- [x] The UI explains that the score is secondary to traceability.
- [x] The UI exposes behavioural eval results and links to repository evidence.
- [x] The UI exposes a DKB-role requirement → proof map.

## Product
- [x] Synthetic card-testing scenario is runnable from the UI/API.
- [x] A suspicious event can create a persisted fraud case.
- [x] Every surfaced signal contains inspectable evidence.
- [x] Human ALLOW / REVIEW / BLOCK decisions are recorded in the audit trail.
- [x] Demo runs are deterministic and reset in-memory scenario state.

## Behavioural proof
- [x] Golden card-testing scenario creates a case with risk score 65.
- [x] Golden card-testing scenario includes `transaction_velocity` and `amount_anomaly`.
- [x] Routine customer activity produces no fraud case.
- [x] Rapid country change plus unseen device produces `impossible_travel` and `new_device` and creates a case.
- [x] Analyst decision creates an `ANALYST_DECISION` audit entry with visible evidence.

## Engineering
- [x] First-class frontend lives in `frontend/`.
- [x] API tests verify frontend, proof endpoint and source traceability.
- [x] Behavioural eval runner covers positive and negative cases.
- [x] CI checks repository contract, tests and evals.
- [x] Build OS files are present and non-empty.
- [ ] Public deployment is healthy and manually smoke-tested.

## Release command

```bash
python scripts/check_build_os.py && pytest -q && python evals/run_evals.py --check
```
