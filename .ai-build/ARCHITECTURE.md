# ARCHITECTURE

## Reviewer flow

```text
Role relevance / 90-second CTA
          ↓
Synthetic source events
          ↓
Explainable fraud case
          ↓
Signal evidence
          ↓
Human decision + audit
          ↓
Executable proof + role mapping
```

## System flow

```text
Synthetic transaction event
          ↓
      FastAPI boundary
          ↓
   deterministic rules
          ↓
 evidence-backed signals
          ↓
       risk score
          ↓
 case threshold (>= 50)
          ↓
 investigator frontend
          ↓
 human decision
          ↓
       audit trail
```

## Components

- `frontend/` — reviewer-facing explanation and investigation UX.
- `app/models.py` — typed domain contracts.
- `app/rules.py` — deterministic signal extraction and score aggregation.
- `app/service.py` — event history, case lifecycle and audit trail.
- `app/proof.py` — role mapping and proof presentation adapter.
- `app/main.py` — REST API, proof endpoint and frontend serving.
- `app/seed.py` — synthetic golden scenario.
- `evals/` — behavioural evaluation across positive and negative scenarios.
- `tests/` — API and behavioural verification.
- `evidence/` — generated proof of eval outcomes.

## Integration boundary
The local service uses in-memory state deliberately. In a real fraud platform these boundaries could map to an event stream, durable case store, analyst workflow and downstream decision API. FraudFlow demonstrates the contract without pretending to implement that infrastructure.

## Trust boundary
Only deterministic rules affect the risk recommendation. A human remains responsible for the final case decision. No LLM is in the control path.

## Proof boundary
The frontend never invents proof status. `/proof/summary` reads committed eval evidence and links reviewers to the underlying repository artifacts.
