# FraudFlow Proof Index

This page answers one question: **what should a reviewer inspect if they want to verify a claim?**

| Claim | Reproducible proof | What it demonstrates |
|---|---|---|
| The repository follows the six-stage Build OS | `python scripts/check_build_os.py` + `.ai-build/` + `AGENTS.md` | explicit process, autonomy and completion gates |
| Card testing creates an evidence-backed case | `tests/test_golden_case.py` + `evals/run_evals.py` | golden-path fraud behaviour |
| Routine behaviour does not create a case | `routine_customer_no_alert` eval | negative-case discipline / false-alert thinking |
| New device + rapid country change is detected | `impossible_travel_takeover` eval | multi-signal behaviour |
| Human decision remains auditable | golden test + `human_decision_audit` eval | human accountability + evidence retention |
| The demo shows the source facts, not just a score | `tests/test_api.py` + `/demo/card-testing` source events | end-to-end traceability |
| The visible proof panel is not hard-coded success theatre | `/proof/summary` reads `evidence/eval-results.json` | evidence-backed presentation |
| The UI is designed for hiring manager, engineer and HR | `.ai-build/USERS.md` + frontend guided journey | explicit user-centred reviewer experience |
| The work maps to the target Tech Analyst responsibilities | `docs/REQUIREMENT_MAP.md` + `app/proof.py` | role-specific proof coverage and honest gaps |
| Current guided-UX release passed automated gates | `evidence/ci-proof.md` + GitHub Actions | Build OS, tests, evals and compile check |

## One-command local verification

```bash
python scripts/check_build_os.py && pytest -q && python evals/run_evals.py --check && python -m compileall -q app evals scripts
```

## Evidence philosophy

A screenshot is presentation, not proof. A green badge is useful, but not sufficient by itself. The strongest evidence here is the combination of:

**explicit acceptance criterion → implementation → executable test/eval → machine-readable result → CI execution → reviewer-facing traceability.**
