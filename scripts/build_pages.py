import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.proof import proof_summary
from app.seed import card_testing_events
from app.service import FraudService
from app.signup_flow import signup_demo_scenarios

FRONTEND = ROOT / "frontend"
DIST = ROOT / "dist"
EVIDENCE = ROOT / "evidence" / "eval-results.json"


def build_scenario() -> dict:
    service = FraudService()
    events = card_testing_events()
    case = None
    for event in events:
        case = service.ingest(event) or case
    if case is None:
        raise RuntimeError("Golden scenario did not create a case")
    return {
        "source_events": [event.model_dump(mode="json") for event in events],
        "case": case.model_dump(mode="json"),
    }


def main() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)

    (DIST / "ui").mkdir(parents=True)
    (DIST / "demo").mkdir(parents=True)

    shutil.copy2(FRONTEND / "index.html", DIST / "index.html")
    shutil.copy2(FRONTEND / "styles.css", DIST / "ui" / "styles.css")
    shutil.copy2(FRONTEND / "app.js", DIST / "ui" / "app.js")
    (DIST / ".nojekyll").write_text("", encoding="utf-8")

    scenario = build_scenario()
    (DIST / "demo" / "scenario.json").write_text(
        json.dumps(scenario, indent=2) + "\n", encoding="utf-8"
    )

    (DIST / "demo" / "signup-flow.json").write_text(
        json.dumps(signup_demo_scenarios(), indent=2) + "\n", encoding="utf-8"
    )

    eval_results = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    (DIST / "demo" / "proof.json").write_text(
        json.dumps(proof_summary(eval_results), indent=2) + "\n", encoding="utf-8"
    )

    print("GitHub Pages artifact built: dist/")


if __name__ == "__main__":
    main()
