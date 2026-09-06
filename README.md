# FraudFlow — DKB Fraud Data & Integration Proof

A role-specific work sample for **Junior Tech Analyst Fraud Data & Analytics**.

> **Goal:** let a hiring manager understand the fraud workflow in under 90 seconds, while giving engineers direct access to the source events, rules, tests, evals, CI and architecture decisions behind it.

## Start here

The reviewer-facing product is the first-class `frontend/` application served by FastAPI.

The guided flow is:

**Source events → Why did a case open? → Signal evidence → Human decision → Executable proof**

The primary demo replays five synthetic card-testing transactions, ending in a €499 escalation. FraudFlow creates an explainable review case from deterministic rules and keeps the human analyst responsible for the final action.

## What makes this a proof rather than a dashboard

The UI exposes two different layers deliberately:

1. **Investigation layer** — raw events, signal evidence, risk reasoning, analyst decision and audit trace.
2. **Verification layer** — behavioural eval results, CI, acceptance criteria, explicit users and DKB-role requirement mapping.

The frontend never manufactures proof status. `/proof/summary` reads the committed behavioural-eval evidence from `evidence/eval-results.json`.

## Explicit users

See `.ai-build/USERS.md`.

- **Hiring manager / fraud lead:** “Does Michael understand the actual Tech Analyst work?”
- **Engineer / platform teammate:** “Can I trace the behaviour and verify it?”
- **Recruiter / HR:** “Why is this relevant and what did Michael build?”

Every major UI section must answer one of five questions:

1. What am I looking at?
2. What should I do next?
3. Why did the system do that?
4. What evidence proves it?
5. How does this map to the role?

## Target-role mapping

| Role responsibility | FraudFlow evidence |
|---|---|
| Translate business requirements into technical requirements | `.ai-build/SPEC.md`, `ACCEPTANCE.md`, typed domain models |
| Analyse data structures, models and cross-system flows | `TransactionEvent → Signal → FraudCase → AuditEntry` architecture |
| REST APIs, event-driven architecture and interface thinking | FastAPI event boundary + explicit Kafka-compatible/non-production boundary |
| Accompany implementation through testing | tests + behavioural evals + CI release gate + runbook |
| Communicate complex topics clearly | guided hiring-manager frontend + role map + explicit users |

## Behavioural proof

The current suite requires all four cases to pass:

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

## Repository structure

```text
fraudflow-dkb/
├── .ai-build/
│   ├── SPEC.md
│   ├── USERS.md
│   ├── ARCHITECTURE.md
│   ├── DECISIONS.md
│   ├── ACCEPTANCE.md
│   ├── AUTONOMY.md
│   ├── EVALS.md
│   ├── RUNBOOK.md
│   └── RETROSPECTIVE.md
├── AGENTS.md
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── app/
│   ├── main.py
│   ├── models.py
│   ├── rules.py
│   ├── service.py
│   ├── proof.py
│   └── seed.py
├── evals/
├── tests/
├── evidence/
├── scripts/
├── .github/workflows/
└── README.md
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
- no real DKB/customer/payment data
- no copied DKB product UI or logo
- no production-banking claim
- no fabricated ML accuracy
- no autonomous fraud blocking
- no production Kafka claim
- no LLM in the decision path

## Application angle

> I build inspectable systems between domain teams and engineering — translating requirements into data contracts, APIs, evidence-backed behaviour, tests and operational hand-off. FraudFlow is a deliberately small fraud-data proof where every important decision can be traced and verified.
