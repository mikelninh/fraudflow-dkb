# RETROSPECTIVE

## 2026-09-06 — V0.2 → Build OS retrofit

### What worked
- A narrow golden path made the fraud workflow understandable quickly.
- Deterministic signals keep the proof honest and inspectable.
- The investigator cockpit turns backend concepts into a reviewer-facing story.

### What was missing
- The process was implicit: architecture, autonomy, eval policy, runbook and retrospective were not first-class artifacts.
- Tests existed, but there was no explicit negative eval suite or CI gate.
- Deployment was not yet part of the acceptance definition.

### Change
Adopted the six-stage Build OS as an enforced repository contract: SHAPE → SPECIFY → DELEGATE → PROVE → SHIP → WATCH.

---

## 2026-09-06 — Reviewer feedback: “not intuitive enough; where are the proofs?”

### Feedback observed
The technically working cockpit was not yet strong enough as a hiring work sample. A reviewer could see a risk score and signals, but the product did not clearly answer:
- who this experience was designed for,
- what to click first,
- what the source facts were,
- why a case opened,
- where the proof behind the claims lived,
- how the work mapped to the DKB role.

### Root cause
The user was under-specified. `SPEC.md` named a fraud analyst, but hiring manager, engineer and recruiter review journeys were not explicit product users. The frontend was implementation output rather than a first-class evidence/communication layer.

### Changes made
- added `.ai-build/USERS.md` with three explicit reviewer personas and success criteria
- made `frontend/` a first-class repo component
- rebuilt the UI around a guided four-step journey: Source → Interpretation → Decision → Proof
- returned raw source events from the demo API so the UI can show traceability
- added `/proof/summary` backed by committed eval evidence
- exposed role requirement → proof mapping
- linked the UI directly to eval evidence, CI, acceptance criteria and Build OS artifacts
- added API tests for frontend assets, proof exposure and source traceability

### Evidence
GitHub Actions run #12 (`34023626647`) passed Build OS contract, tests, behavioural evals and compile checks for the first guided-UX commit.

### Still to prove
- manual browser smoke test of the deployed public version
- blind review: can a hiring manager explain the proof after <90 seconds?
- engineer review: can a teammate locate the source evidence and known gaps without guidance?

### Principle
A portfolio proof has two products: the system being demonstrated and the reviewer experience that makes its evidence legible.
