# DECISIONS

## D-001 — Deterministic core over fake ML
**Decision:** Use inspectable rules and additive risk scoring.
**Why:** The work sample should prove reasoning and integration, not fabricate model performance.

## D-002 — Human final decision
**Decision:** FraudFlow recommends REVIEW/BLOCK but never autonomously finalises a fraud action.
**Why:** High-stakes decisions need accountable human review in this proof.

## D-003 — Synthetic data only
**Decision:** All events, customers, devices, IPs and merchants are synthetic.
**Why:** The project is public and should be safe to inspect and run.

## D-004 — Event-shaped API without claiming Kafka
**Decision:** Model the ingestion boundary as events and REST endpoints while keeping the implementation local.
**Why:** It shows event-stream thinking honestly without claiming production Kafka experience.

## D-005 — Build OS is part of the proof
**Decision:** SHAPE → SPECIFY → DELEGATE → PROVE → SHIP → WATCH is enforced through repository structure and CI.
**Why:** The engineering process itself is relevant evidence for an analyst/engineering role.

## D-006 — Frontend is a first-class repository component
**Decision:** Move the reviewer experience into `frontend/` rather than treating UI as a decorative static page.
**Why:** A hiring manager should not need repository knowledge to understand the proof; engineers should still be able to trace every visible claim to code/evidence.

## D-007 — Explicit reviewer users
**Decision:** Treat hiring manager/fraud lead, engineer/platform teammate and recruiter/HR as explicit users in `.ai-build/USERS.md`.
**Why:** The previous cockpit was technically functional but not sufficiently intuitive because it had no documented review journey.

## D-008 — Proof must be visible in-product
**Decision:** Add a proof surface backed by committed eval evidence and direct links to CI, acceptance criteria and repository artifacts.
**Why:** A work sample should not ask the reviewer to trust screenshots or prose; claims should lead to reproducible evidence.

## D-009 — DKB-aligned, not DKB-impersonating
**Decision:** Use a clear high-contrast, finance/tech-oriented visual language with a yellow accent, but no DKB logo or copied product interface.
**Why:** The work should feel intentionally prepared for the target team while remaining clearly the candidate's own artifact.
