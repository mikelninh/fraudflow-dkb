# AUTONOMY

## Agents may autonomously
- refactor code without changing documented behaviour
- add tests and eval scenarios
- improve UI clarity and accessibility
- strengthen validation and error handling
- update documentation to reflect verified behaviour
- fix CI/deployment configuration when acceptance criteria stay unchanged

## Agents must stop or require human judgement before
- changing the definition of fraud/risk thresholds as a product policy
- introducing real customer or bank data
- adding autonomous blocking/execution
- weakening evidence/audit requirements
- adding credentials, secrets or paid infrastructure
- claiming production banking, Kafka or ML experience not demonstrated here
- deleting or loosening acceptance criteria to make a failing build pass

## Evidence rule
Agents may generate evidence only by executing tests/evals or by directly inspecting a deterministic artifact. Never manufacture benchmark results.

## Scope rule
Prefer the smallest change that closes an acceptance gap. Do not turn a targeted work sample into a speculative bank platform.
