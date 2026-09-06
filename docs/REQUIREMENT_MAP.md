# DKB Junior Tech Analyst Fraud Data & Analytics — Proof Map

This file maps the target responsibilities to inspectable repository evidence. It is intentionally specific: gaps are stated rather than hidden.

| Target responsibility / skill | Evidence in FraudFlow | Status |
|---|---|---|
| Capture business + technical processes and translate requirements for developers | `.ai-build/SPEC.md`, `.ai-build/ACCEPTANCE.md`, typed `TransactionEvent` / `FraudCase` contracts | Demonstrated |
| Accompany work from requirements through testing | Build OS, API tests, behavioural eval suite, CI release gate, runbook | Demonstrated |
| Analyse data structures, models and cross-system data flows | `ARCHITECTURE.md` plus event → signal → case → audit flow | Demonstrated |
| Integrate services and interfaces in an event-driven architecture | Event-shaped FastAPI ingestion boundary; documented future event-stream boundary | Demonstrated at proof level |
| Clarify REST APIs, event streams and synchronous/asynchronous interfaces | REST endpoints + architecture/decision docs | REST demonstrated; event-stream concepts only |
| Git / GitHub | Repo, commits, GitHub Actions | Demonstrated |
| Python | FastAPI backend, deterministic rule engine, eval runner | Demonstrated |
| Testing / technical acceptance | Golden, negative, adversarial and API tests | Demonstrated |
| Communicate complex technical topics clearly | First-class guided frontend and explicit reviewer users | Demonstrated |
| SQL / BI tools | Not used in this intentionally narrow proof | Gap / address in application |
| Kafka production experience | Architecture-compatible concepts only; no production claim | Gap / learning target |
| Cloud data pipelines | Deployment + integration concepts, not a real bank data platform | Partial |

## Strongest story

The value of the work sample is not “I built a fraud detector”. It is:

> I can take an ambiguous fraud workflow, define its users and acceptance criteria, express the data contracts and interfaces, build an inspectable implementation, prove expected/negative behaviour, and communicate the result to both domain and engineering reviewers.
