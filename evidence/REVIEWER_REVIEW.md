# Reviewer review — 2026-09-06

This review treats the work sample as a product for three different reviewers rather than as a developer dashboard.

## HR / recruiter — first 20 seconds

### Question
Can a non-technical reviewer explain what Michael built and why it matters?

### Finding
The earlier version still exposed too much implementation language up front: risk points, case IDs, traceability chains, API boundaries and audit terminology competed with the actual story.

### Change
- lead with one plain-language fraud scenario
- explain the value as `problem understood → clear decision support → behaviour verified`
- use one obvious CTA
- keep technical details out of the primary path
- replace `Behavioural Evals` as the main label with `Prüfszenarien`

### Pass condition
After ~20 seconds a reviewer should be able to say: “Five unusual payments are explained clearly, the system recommends a review, and a human still decides.”

## Hiring manager / fraud lead — first 90 seconds

### Question
Does the work sample demonstrate role-relevant judgement rather than generic dashboard work?

### Finding
The strongest story is not the internal score. It is the transition from ordinary-looking source data to an explainable reason for review, followed by a human decision.

### Change
- show source payments before interpretation
- mark only the final trigger event as suspicious
- explain the two reasons in plain language
- explicitly state that FraudFlow does not claim to have “detected fraud”
- add a direct path from the analyst decision to the proof section
- keep the DKB requirement-to-proof mapping below the main journey

### Pass condition
Within ~90 seconds the reviewer should understand the case, why it surfaced, the human-control boundary, and where to verify the behaviour.

## Engineer / platform teammate — first 5 minutes

### Question
Can an engineer verify that the story is technically coherent and honestly scoped?

### Finding
Technical depth should remain available without forcing HR through it. A shareable static reviewer demo also needs to be explicit about the boundary between presentation and executable backend proof.

### Change
- keep case ID, risk score, rule counts and event counts under expandable engineer details
- keep FastAPI, tests, evals, CI, architecture and evidence in the repository
- build the GitHub Pages demo from the same synthetic seed and eval evidence
- show a note in engineer details when running on GitHub Pages: the browser demo is a fixed synthetic playback; the backend implementation and verification remain executable in the repo
- gate the Pages artifact behind the same Build OS, tests and evals

### Pass condition
An engineer can trace `source event → deterministic rule evidence → case → human decision → audit`, inspect the relevant implementation, and reproduce the proof locally or in CI.

## Overall decision

The work sample should optimize for **progressive disclosure**:

**HR clarity first → hiring-manager reasoning second → engineer depth on demand.**

If the reviewer has to understand the architecture before understanding the problem, the UX has failed.
