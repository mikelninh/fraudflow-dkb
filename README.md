# FraudFlow — Fraud Operations & Decision Systems

A reusable proof-of-work for **fraud data, prevention, controls and platform roles**.

> **Goal:** let a non-technical reviewer understand the fraud workflow quickly, while giving engineers direct access to the source events, data-quality layer, SQL/Python analysis, rules, tests, evals, CI and architecture decisions behind it.

FraudFlow is deliberately **company-neutral**. The same verified product can support different applications without turning the repository or UI into a branded hiring exercise.

## Start here

The reviewer-facing product is the first-class `frontend/` application served by FastAPI and built to GitHub Pages.

The guided flow is:

**Source payments → data quality → plain-language reasons → human decision → monitoring → reproducible proof**

The primary demo replays five synthetic card-testing transactions, ending in a €499 escalation. FraudFlow creates an explainable review case from deterministic rules and keeps the human analyst responsible for the final action.

## What makes this a proof rather than a dashboard

The UI exposes three layers deliberately:

1. **Reviewer layer** — what happened, why it is unusual, and what a human should do next.
2. **Data & Technology layer** — how synthetic events pass through quality checks, typed data, SQL/Python analysis, fraud signals and KPI monitoring.
3. **Verification layer** — source evidence, behavioural eval results, CI, acceptance criteria and architecture decisions.

The frontend never manufactures proof status. `/proof/summary` reads committed behavioural-eval evidence from `evidence/eval-results.json`, while the data-tech metrics are generated deterministically at build time from `analysis/data_tech_lab.py`.

## Explicit users

See `.ai-build/USERS.md`.

- **Hiring manager / fraud lead:** “Does Michael understand fraud operations well enough to translate them into a reliable system?”
- **Engineer / platform teammate:** “Can I trace the behaviour, data flow and verification boundary?”
- **Recruiter / HR:** “What did Michael build, why is it useful, and where could this apply?”

## Reusable capability map

| Capability | FraudFlow evidence |
|---|---|
| Fraud Data & Analytics | deterministic synthetic cohort + SQL/Python metrics + explainable transaction signals |
| Business Analysis | source events → requirements/flow → review case → measurable outcome |
| Data Quality | explicit completeness gate + tested data-quality pass metric |
| Fraud Prevention & Controls | explainable patterns + negative cases + human review |
| Platform & Integration | FastAPI boundaries + typed models + event-oriented contracts |
| Monitoring | alert volume/rate, analyst outcomes, signal distribution and reproducible build evidence |
| Governance & Auditability | evidence → human decision → audit + reproducible proof |
| Communication & Product Thinking | plain-language reviewer journey + engineer deep dive |

The **application** can emphasize different rows. The **product and evidence remain the same**.

## Data & Technology evidence

- `analysis/data_tech_lab.py` — deterministic synthetic transaction cohort, SQLite data flow and KPI generation
- `analysis/fraud_metrics.sql` — example SQL for data quality, alert rate, outcomes and segment monitoring
- `tests/test_data_tech_analysis.py` — deterministic and bounded analytics contract
- `dist/demo/data-tech-summary.json` — generated Pages evidence, never hand-authored by the frontend

This layer deliberately does **not** claim production Kafka, a production fraud model, or real bank data. It demonstrates the translation from events and data quality into measurable fraud operations.

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
python -m compileall -q app analysis evals scripts
```

## Architecture

```text
Source events
   │
   ├──► data-quality / analytics layer ──► monitoring evidence
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

- **data / tech analyst lens:** data flows, APIs, models, data quality, SQL/Python analysis, testing and monitoring
- **fraud prevention / AFC lens:** anomalies, controls, human review, KRIs and documentation
- **fraud platform lens:** integrations, evidence contracts, reliability and operational hand-off

> I build inspectable systems between fraud operations and engineering — translating messy behaviour into evidence-backed signals, data flows, human decisions, APIs, tests and auditability.
