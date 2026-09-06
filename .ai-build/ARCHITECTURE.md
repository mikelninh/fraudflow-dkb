# ARCHITECTURE

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
 investigator cockpit
          ↓
 human decision
          ↓
       audit trail
```

## Components

- `app/models.py` — typed domain contracts.
- `app/rules.py` — deterministic signal extraction and score aggregation.
- `app/service.py` — event history, case lifecycle and audit trail.
- `app/main.py` — REST API and demo entrypoint.
- `app/static/index.html` — investigator cockpit.
- `app/seed.py` — synthetic golden scenario.
- `evals/` — behavioural evaluation across positive and negative scenarios.
- `tests/` — unit/integration verification.
- `evidence/` — generated proof of eval outcomes.

## Integration boundary
The local service uses in-memory state deliberately. In a real fraud platform these boundaries could map to an event stream, durable case store, analyst workflow and downstream decision API. FraudFlow demonstrates the contract without pretending to implement that infrastructure.

## Trust boundary
Only deterministic rules affect the risk recommendation. A human remains responsible for the final case decision. No LLM is in the control path.
