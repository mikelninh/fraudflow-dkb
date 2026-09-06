# SPEC — FraudFlow

## Problem
Fraud analysts need to move from raw transaction events to a reviewable decision without losing the evidence that explains why a case was surfaced.

## Primary user
A fraud/data analyst integrating or operating fraud-detection services in a banking environment.

## Job-to-be-done
Given synthetic payment events, surface suspicious behaviour as an explainable case, show the exact signals and source evidence, allow a human decision, and retain an audit trail.

## In scope
- typed transaction-event ingestion
- deterministic fraud signals
- evidence-backed risk scoring
- case creation and retrieval
- human ALLOW / REVIEW / BLOCK decision
- audit trail
- investigator cockpit
- synthetic golden and negative scenarios
- CI, evals and reproducible evidence

## Explicit non-goals
- production fraud detection
- real DKB/customer/payment data
- claims of Kafka production experience
- black-box ML accuracy claims
- autonomous account blocking
- replacing an investigator or existing bank control system

## Constraints
- Python + FastAPI
- small, inspectable architecture
- no secrets or external paid services required
- deterministic decision path
- deployable as a public proof-of-work

## Success
A reviewer can understand the system in under 90 seconds and verify that the golden fraud scenario produces an evidence-backed case while routine activity does not.
