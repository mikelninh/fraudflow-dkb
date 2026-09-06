# AGENTS.md — FraudFlow Build Contract

This repository follows Michael Ninh's six-stage AI Build OS. For serious portfolio and production work this process is the default, not optional ceremony.

## 01 SHAPE
Before implementation, understand the problem, user, constraints and system boundary. Update `.ai-build/SPEC.md` and `.ai-build/ARCHITECTURE.md` when those assumptions change.

## 02 SPECIFY
Turn intent into explicit requirements, non-goals and acceptance criteria. Work is not complete because code exists; it is complete when `.ai-build/ACCEPTANCE.md` is satisfied.

## 03 DELEGATE
Agents may implement within the limits in `.ai-build/AUTONOMY.md`. Do not invent product requirements, weaken safety boundaries, fabricate evidence, or silently change acceptance criteria.

## 04 PROVE
Run tests, evals and adversarial/golden cases. Store reproducible evidence in `evidence/`. Never claim a capability that has not been tested or directly inspected.

## 05 SHIP
CI is a release gate. A deploy is allowed only after tests, evals and the Build OS structure pass. Deployment instructions live in `.ai-build/RUNBOOK.md`.

## 06 WATCH
Treat traces, logs, regressions and user feedback as inputs to the next build cycle. Record material findings and follow-ups in `.ai-build/RETROSPECTIVE.md` and `.ai-build/DECISIONS.md`.

## Non-negotiables

- Synthetic data only in this proof-of-work.
- No LLM or agent may make the final fraud blocking decision.
- Evidence attached to a signal must come from input data or deterministic computation.
- Keep the system small enough to inspect end-to-end.
- Prefer an honest missing capability over a fake production claim.
- Any material behaviour change needs tests/evals and a decision note.

## Completion gate

Before saying a task is finished:

1. `python scripts/check_build_os.py`
2. `pytest -q`
3. `python evals/run_evals.py --check`
4. confirm the relevant acceptance criteria
5. update evidence/retrospective when behaviour materially changed
