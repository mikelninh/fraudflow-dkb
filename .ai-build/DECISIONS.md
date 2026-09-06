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
