# ACCEPTANCE

FraudFlow is release-ready only when all critical criteria pass.

## User experience
- [x] Explicit users are documented in `.ai-build/USERS.md`.
- [x] UX principles live in `docs/UX_PRINCIPLES.md`.
- [x] Root route explains role relevance before asking the reviewer to interact.
- [x] There is one obvious primary CTA: `90-Sekunden-Fall starten`.
- [x] A reviewer needs no prior fraud knowledge to understand the demo.
- [x] The default journey answers: what happened → why unusual → what next → where is the proof.
- [x] Plain-language reasons are shown before technical terms or internal scores.
- [x] Case ID, risk score and rule metadata are progressive-disclosure details for engineers.
- [x] Raw source payments remain visible and traceable.
- [x] Only the final trigger payment is visually marked as suspicious in the golden case.
- [x] The UI exposes behavioural eval results and links to repository evidence.
- [x] The UI exposes a DKB-role requirement → proof map.
- [x] The interface labels itself as an independent work sample and does not use protected DKB logo assets.
- [x] HR, hiring-manager and engineer review findings are documented in `evidence/REVIEWER_REVIEW.md`.

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
- [x] CI checks repository contract, tests, evals and the static reviewer artifact.
- [x] `scripts/build_pages.py` generates the GitHub Pages site from the same synthetic seed and committed eval evidence.
- [x] `.github/workflows/pages.yml` gates deployment behind Build OS, tests and evals.
- [x] Build OS files are present and non-empty.
- [ ] GitHub Pages deployment is healthy and manually smoke-tested.

## Release command

```bash
python scripts/check_build_os.py && pytest -q && python evals/run_evals.py --check && python scripts/build_pages.py
```
