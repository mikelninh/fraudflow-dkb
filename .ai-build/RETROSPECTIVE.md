# RETROSPECTIVE

## 2026-09-06 — V0.2 → Build OS retrofit

### What worked
- A narrow golden path made the fraud workflow understandable quickly.
- Deterministic signals keep the proof honest and inspectable.
- The investigator cockpit turns backend concepts into a reviewer-friendly story.

### What was missing
- The process was implicit: architecture, autonomy, eval policy, runbook and retrospective were not first-class artifacts.
- Tests existed, but there was no explicit negative eval suite or CI gate.
- Deployment was not yet part of the acceptance definition.

### Change
Adopted the six-stage Build OS as an enforced repository contract: SHAPE → SPECIFY → DELEGATE → PROVE → SHIP → WATCH.

### Next evidence to seek
- successful CI run
- live deployment smoke test
- reviewer feedback on whether the fraud case is understandable in <90 seconds

### Principle
The repository should not merely say that a system is reliable; it should leave inspectable evidence of how reliability was established.
