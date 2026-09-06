# SPEC — FraudFlow

## Problem
Fraud analysts need to move from raw transaction events to a reviewable decision without losing the evidence that explains why a case was surfaced. A hiring reviewer also needs to understand that proof quickly without reading the repository first.

## Users
See `.ai-build/USERS.md`. The product explicitly serves:
- hiring manager / fraud lead,
- engineer / platform teammate,
- recruiter / HR.

## Primary job-to-be-done
Given synthetic payment events, surface suspicious behaviour as an explainable case, show the exact signals and source evidence, allow a human decision, and retain an audit trail.

## Review job-to-be-done
Within 90 seconds, a DKB reviewer should be able to understand the scenario, why a case surfaced, what the analyst does next, and where the executable proof lives.

## In scope
- first-class frontend in `frontend/`
- guided 90-second investigation
- typed transaction-event ingestion
- deterministic fraud signals
- evidence-backed risk scoring
- case creation and retrieval
- human ALLOW / REVIEW / BLOCK decision
- audit trail
- visible source-event → signal → case traceability
- visible behavioural proof and role-requirement mapping
- synthetic golden and negative scenarios
- CI, evals and reproducible evidence

## Explicit non-goals
- production fraud detection
- real DKB/customer/payment data
- copying or impersonating DKB's product UI or logo
- claims of Kafka production experience
- black-box ML accuracy claims
- autonomous account blocking
- replacing an investigator or existing bank control system

## Constraints
- Python + FastAPI backend
- dependency-light frontend served by the same app
- small, inspectable architecture
- no secrets or external paid services required
- deterministic decision path
- deployable as a public proof-of-work

## Success
- hiring manager understands the work sample in <90 seconds
- engineer can trace every alert back to source facts
- recruiter can explain why it maps to the target role
- all behavioural evals and CI gates pass
