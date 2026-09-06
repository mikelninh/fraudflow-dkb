# FraudFlow — Fraud Data & Integration Lab

A targeted proof-of-work for a **Junior Tech Analyst Fraud Data & Analytics** role.

FraudFlow demonstrates a small, inspectable fraud workflow:

**Transaction event → deterministic signals → evidence-backed case → human decision → audit trail**

The project uses **synthetic data only**. It intentionally avoids black-box “AI detects fraud” claims and instead shows how data, integration boundaries, evidence and analyst review can fit together.

## Golden demo

The main scenario simulates card testing followed by escalation:

```text
09:41:02  €1.00
09:41:08  €1.00
09:41:14  €2.00
09:41:21  €1.00
09:41:29  €499.00
```

Expected behaviour:

- transaction velocity fires,
- the final amount is anomalous versus the synthetic customer baseline,
- FraudFlow creates a review case,
- every signal exposes the evidence that produced it,
- a human analyst can choose `ALLOW`, `REVIEW` or `BLOCK`,
- the decision and visible evidence are retained in the audit trail.

A separate behavioural eval covers **new device + impossible travel**. Routine synthetic activity is also tested as a negative case and must produce no fraud case.

## What this proves

### Event and integration thinking

The API is shaped around realistic system boundaries:

```text
POST /events/transaction
GET  /cases/{case_id}
POST /cases/{case_id}/decision
GET  /cases/{case_id}/audit
```

The implementation is deliberately local and lightweight. These contracts could sit behind an event-stream architecture such as Kafka, but this project does **not** claim production Kafka experience.

### Explainable signals

Signals are deterministic and inspectable. Current examples include:

- transaction velocity,
- amount anomaly,
- new device,
- impossible travel.

Each signal carries the exact synthetic evidence used to derive it.

### Human-in-the-loop decisions

FraudFlow can recommend `REVIEW` or `BLOCK`, but the proof does not autonomously finalise a high-stakes fraud action. A human reviewer remains accountable for the final decision.

### Evidence-first investigation

The goal is not merely to produce a risk score. The reviewer should be able to answer:

- what happened,
- which signals fired,
- what evidence supports them,
- what should be reviewed next,
- who made the final decision,
- and what evidence was visible at that moment.

## How I Build

Every serious portfolio or production project follows the same six-stage system:

**01 SHAPE** — Problem → user → constraints → architecture

**02 SPECIFY** — Requirements → boundaries → acceptance criteria

**03 DELEGATE** — Agents execute within explicit autonomy limits

**04 PROVE** — Tests → evals → benchmarks → adversarial cases

**05 SHIP** — CI → deployment gates → production

**06 WATCH** — Traces → logs → regressions → feedback

FraudFlow makes that process inspectable in the repository rather than leaving it as a claim.

## Repository contract

```text
fraudflow-dkb/
├── .ai-build/
│   ├── SPEC.md
│   ├── ARCHITECTURE.md
│   ├── DECISIONS.md
│   ├── ACCEPTANCE.md
│   ├── AUTONOMY.md
│   ├── EVALS.md
│   ├── RUNBOOK.md
│   └── RETROSPECTIVE.md
├── AGENTS.md
├── app/
├── evals/
├── tests/
├── evidence/
├── scripts/
├── .github/
│   └── workflows/
│       └── ci.yml
├── pyproject.toml
├── vercel.json
├── requirements.txt
└── README.md
```

`AGENTS.md` is the operating contract for coding agents. It defines the six stages, autonomy boundaries and completion gate.

`scripts/check_build_os.py` fails CI if the required Build OS structure is missing or empty.

## Proof, not promises

The release gate is:

```bash
python scripts/check_build_os.py
pytest -q
python evals/run_evals.py --check
python -m compileall -q app evals scripts
```

GitHub Actions executes the same checks on pushes and pull requests.

The behavioural suite currently verifies:

| Scenario | Expected result |
|---|---|
| Card testing → escalation | case created, risk 65, velocity + amount anomaly |
| Routine customer activity | no case |
| Berlin → Singapore + new device in 30 min | case created, risk 70, impossible travel + new device |
| Human review | decision + visible evidence retained in audit trail |

Reproducible output is stored under `evidence/`.

## Architecture

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

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/` for the investigator cockpit or `/docs` for the API.

## Deliberate boundaries

- synthetic data only,
- no real DKB/customer/payment data,
- no fabricated model accuracy,
- no autonomous fraud blocking,
- no claim that this is a production banking platform,
- no LLM in the fraud decision path.

The point is to make the reasoning, interfaces, evidence and engineering process easy to inspect.

## Portfolio connection

FraudFlow applies patterns from my evidence-grounded systems work to fraud operations: entity/evidence thinking, signal reliability, reproducibility, human review and auditable decisions.

## Application angle

> I build inspectable data systems between domain teams and engineering — from API and data model to signal, human review and audit trail. FraudFlow is a deliberately small synthetic proof showing how I reason about integrating and operationalising fraud signals without hiding decisions behind black-box AI.
