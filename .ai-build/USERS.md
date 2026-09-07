# USERS — FraudFlow

FraudFlow has three explicit review users. The product and proof surface must work for all three without company-specific context.

## U1 — Hiring manager / fraud lead

**Question in the first 30 seconds:** Does Michael understand fraud operations well enough to translate them into a reliable, reviewable system?

Needs to see:
- the business problem in plain language
- one obvious action to start the demo
- a realistic fraud scenario, not generic AI
- why a case was created
- what the analyst can do next
- visible evidence of data, control and integration thinking

Success condition:
- understands the demo in under 90 seconds
- can name at least three fraud-relevant capabilities demonstrated

## U2 — Engineer / platform teammate

**Question in the first 60 seconds:** Is this technically coherent and honest?

Needs to see:
- event shape and API boundaries
- deterministic rule logic and thresholds
- exact source evidence for each signal
- human decision boundary
- tests, behavioural evals, CI and architecture decisions
- clear non-goals and production limitations

Success condition:
- can trace an alert from source events → signals → case → decision → audit
- can inspect reproducible proof without trusting screenshots or claims

## U3 — Recruiter / HR

**Question in the first 20 seconds:** What did Michael build, why is it useful, and where could this work apply?

Needs to see:
- purpose immediately
- short explanation without fraud jargon overload
- compact proof summary
- a clear story that works across fraud data, prevention, controls and platform roles

Success condition:
- can explain the project to a hiring manager after a short visit

## UX rule

Every major screen should answer one of these questions:
1. What am I looking at?
2. What should I do next?
3. Why did the system do that?
4. What evidence proves it?
5. Which reusable fraud capability does this demonstrate?

If a screen does not help answer one of them, it is probably noise.
