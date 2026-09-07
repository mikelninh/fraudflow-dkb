# FraudFlow — Fraud Operations & Decision Systems

A reusable proof-of-work for **fraud data, prevention, controls and platform roles**.

> **Goal:** let a non-technical reviewer understand the fraud workflow quickly, while giving engineers direct access to the source events, rules, tests, evals, CI and architecture decisions behind it.

FraudFlow is deliberately **company-neutral**. The same verified product can support different applications without turning the repository or UI into a branded hiring exercise.

## Start here

The reviewer-facing product is the first-class `frontend/` application served by FastAPI and built to GitHub Pages.

The guided flow is:

**Source payments → plain-language reasons → human decision → reproducible proof**

The primary demo replays five synthetic card-testing transactions, ending in a €499 escalation. FraudFlow creates an explainable review case from deterministic rules and keeps the human analyst responsible for the final action.

## What makes this a proof rather than a dashboard

The UI exposes two layers deliberately:

1. **Reviewer layer** — what happened, why it is unusual, and what a human should do next.
2. **Verification layer** — source evidence, behavioural eval results, CI, acceptance criteria and architecture decisions.

The frontend never manufactures proof status. `/proof/summary` reads committed behavioural-eval evidence from `evidence/eval-results.json`.

## Explicit users

See `.ai-build/USERS.md`.

- **Hiring manager / fraud lead:** “Does Michael understand fraud operations well enough to translate them into a reliable system?”
- **Engineer / platform teammate:** “Can I trace the behaviour and verify it?”
- **Recruiter / HR:** “What did Michael build, why is it useful, and where could this apply?”

## Reusable capability map

| Capability | FraudFlow evidence |
|---|---|
| Fraud Data & Analytics | typed payment events → deterministic signals → review case |
| Fraud Prevention & Controls | explainable patterns + negative cases + human review |
| Platform & Integration | FastAPI boundaries + typed models + event-oriented contracts |
| Governance & Auditability | evidence → human decision → audit + reproducible proof |
| Communication & Product Thinking | plain-language reviewer journey + engineer deep dive |

The **application** can emphasize different rows. The **product and evidence remain the same**.

## Behavioural proof

The suite requires all four cases to pass:

| Eval | Expected result |
|---|---|
| Card testing → escalation | case, risk 65, velocity + amount anomaly |
| Routine customer | no fraud case |
| Impossible travel + new device | case, risk 70, both signals present |
| Human decision | audit retains final decision and visible evidence |

Run:

```bash
python scripts/check_build_os.py
pytest -q
python evals/run_evals.py --check
python scripts/build_pages.py
python -m compileall -q app evals scripts
```

## Architecture

```text
Reviewer
   │
   ▼
frontend/
   │
   ├──────────────► /proof/summary ──► committed eval evidence
   │
   ▼
FastAPI
   │
   ▼
TransactionEvent
   │
   ▼
deterministic rules
   │
   ▼
evidence-backed signals
   │
   ▼
FraudCase
   │
   ▼
human decision
   │
   ▼
AuditEntry
```

## How I Build

**01 SHAPE** — Problem → user → constraints → architecture

**02 SPECIFY** — Requirements → boundaries → acceptance criteria

**03 DELEGATE** — Agents execute within explicit autonomy limits

**04 PROVE** — Tests → evals → benchmarks → adversarial cases

**05 SHIP** — CI → deployment gates → production

**06 WATCH** — Traces → logs → regressions → feedback

The process is enforced by `AGENTS.md`, `scripts/check_build_os.py` and CI rather than relying on memory.

## Deliberate honesty

- synthetic data only
- no real bank/customer/payment data
- no copied company product UI or logo
- no production-banking claim
- no fabricated ML accuracy
- no autonomous fraud blocking
- no production Kafka claim
- no LLM in the decision path

## Application principle

Do not fork FraudFlow for every company.

Instead, keep one verified core and change only the application narrative:

- **data / tech analyst lens:** data flows, APIs, models, event boundaries, testing
- **fraud prevention / AFC lens:** anomalies, controls, human review, KRIs and documentation
- **fraud platform lens:** integrations, evidence contracts, reliability and operational hand-off

> I build inspectable systems between fraud operations and engineering — translating messy behaviour into evidence-backed signals, human decisions, APIs, tests and auditability.
