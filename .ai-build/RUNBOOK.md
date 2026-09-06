# RUNBOOK

## Local start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/`.

## Pre-release gate

```bash
python scripts/check_build_os.py
pytest -q
python evals/run_evals.py --check
```

Do not deploy on a red gate.

## Smoke test after deploy
1. `GET /health` returns `{"status":"ok"}`.
2. `/` renders the investigator cockpit.
3. Click **Inject card-testing scenario**.
4. Confirm a review case appears with multiple evidence-backed signals.
5. Choose a human decision and confirm the audit trail updates.

## Failure handling
- Build failure: inspect dependency/runtime logs before changing code.
- 404 at root: verify FastAPI entrypoint/routing.
- UI loads but API fails: inspect function runtime logs and relative fetch paths.
- Golden scenario fails: do not weaken the eval; inspect rule or state regression.

## Rollback
Re-deploy the last green commit. Never hot-fix by removing an acceptance or evidence requirement.
