# FraudFlow — Fraud Data & Integration Lab

A small proof-of-work for a **Junior Tech Analyst Fraud Data & Analytics** role.

FraudFlow demonstrates how a suspicious payment can move through an explainable, auditable workflow:

**Event → Validation → Fraud Signals → Risk Decision → Human Review → Audit Trail**

The project uses **synthetic data only**. It is intentionally small, deterministic and inspectable rather than a black-box “AI detects fraud” demo.

## Why this exists

Fraud teams need more than a score. They need to understand:

- what happened,
- which signals fired,
- what evidence supports each signal,
- what data is missing or low quality,
- what an analyst should review next,
- and how the final decision is recorded for later audit.

FraudFlow focuses on that operational layer.

## Golden scenario: card testing → escalation

The demo contains a deliberately simple synthetic attack pattern:

1. a new device appears,
2. several low-value authorisation attempts arrive in rapid succession,
3. transaction velocity crosses a threshold,
4. a much larger follow-up transaction is attempted,
5. FraudFlow opens a review case with evidence-backed signals.

Example sequence:

```text
09:41:02  €1.00
09:41:08  €1.00
09:41:14  €2.00
09:41:21  €1.00
09:41:29  €499.00
```

Expected decision: `REVIEW` or `BLOCK`, depending on the configured threshold.

## What the demo proves

### 1. Event-driven thinking

FraudFlow models a small payment/event flow rather than a static CSV-only analysis.

Example event types:

```text
transaction.created
device.changed
payment.authorized
velocity.threshold_exceeded
```

The implementation is local and lightweight, but the boundary is deliberately compatible with an event-stream architecture such as Kafka.

### 2. Explainable fraud signals

Each signal includes the exact evidence used to derive it.

| Signal | Example evidence | Confidence |
|---|---|---|
| New device | first_seen = 09:40:51 | High |
| Velocity | 5 attempts / 27 sec | High |
| Amount anomaly | 17.3× customer baseline | Medium |
| Impossible travel | Berlin → Singapore in 47 min | High |

No LLM is allowed to invent fraud evidence or finalise a decision.

### 3. Human-in-the-loop review

A reviewer can choose:

- `ALLOW`
- `REVIEW`
- `BLOCK`

The system records who decided, when, why, and which evidence was visible at decision time.

### 4. Integration boundaries

The proof exposes a small REST interface designed around realistic integration points:

```text
POST /events/transaction
GET  /cases/{case_id}
POST /cases/{case_id}/decision
GET  /cases/{case_id}/audit
```

### 5. Evidence-first investigation

The case view links:

```text
CUSTOMER
   │
 DEVICE ───── IP
   │
 ACCOUNT
   │
 TRANSACTION ─── MERCHANT
```

This is intentionally aligned with investigative workflows: the analyst should be able to trace a decision back to entities, signals and source events.

## Architecture

```text
Synthetic Banking Service
          │
          ▼
   Transaction Event
          │
          ▼
   Validation Layer
          │
          ▼
     Signal Engine
   ┌──────┼────────┐
   │      │        │
Device  Velocity  Amount
   │      │        │
   └──────┴────────┘
          │
          ▼
     Risk Decision
          │
          ▼
      Fraud Case
          │
          ▼
      Human Review
          │
          ▼
       Audit Log
```

## Repository structure

```text
fraudflow-dkb/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── rules.py
│   ├── service.py
│   └── seed.py
├── tests/
│   └── test_golden_case.py
├── docs/
│   └── REQUIREMENT_MAP.md
├── requirements.txt
└── README.md
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Run the proof

Create the synthetic card-testing case:

```bash
curl -X POST http://127.0.0.1:8000/demo/card-testing
```

Then inspect it:

```bash
curl http://127.0.0.1:8000/cases/<case_id>
```

Record the analyst decision:

```bash
curl -X POST http://127.0.0.1:8000/cases/<case_id>/decision \
  -H "Content-Type: application/json" \
  -d '{"decision":"BLOCK","analyst":"demo-analyst","reason":"Card-testing pattern followed by high-value attempt"}'
```

## Verification

```bash
pytest -q
```

The golden-case test asserts that the attack sequence produces:

- a persisted fraud case,
- the expected high-value signals,
- a non-allow risk decision,
- evidence attached to every signal,
- and an auditable human decision.

## Deliberate design choices

**Synthetic data only** — no real customer or payment data.

**Deterministic core** — fraud signals are inspectable rules, not fabricated model output.

**LLM-free decision path** — language models can be useful around investigation and summarisation, but they are not required for this proof and do not control blocking decisions.

**Small scope** — the goal is to prove fraud-data integration, technical analysis and explainability, not pretend to rebuild a bank fraud platform.

## Portfolio connection

FraudFlow extends ideas from my other evidence-grounded systems work:

- **SafeTrace** — entity resolution and evidence chains
- **SignalLab** — data quality, signals, drift and human review
- **GitLaw** — traceable evidence and reproducibility

FraudFlow applies those principles to a fraud-operations workflow.

## Application angle

> I build inspectable data systems between domain teams and engineering — from API and data model to signal, human review and audit trail. FraudFlow is a deliberately small synthetic proof showing how I would reason about integrating and operationalising fraud signals without hiding decisions behind black-box AI.
