from pathlib import Path

REQUIRED = [
    "AGENTS.md",
    ".ai-build/SPEC.md",
    ".ai-build/ARCHITECTURE.md",
    ".ai-build/DECISIONS.md",
    ".ai-build/ACCEPTANCE.md",
    ".ai-build/AUTONOMY.md",
    ".ai-build/EVALS.md",
    ".ai-build/RUNBOOK.md",
    ".ai-build/RETROSPECTIVE.md",
    ".ai-build/USERS.md",
    "frontend/index.html",
    "frontend/styles.css",
    "frontend/app.js",
    "evals/run_evals.py",
    "tests/test_golden_case.py",
    "tests/test_api.py",
    "evidence/README.md",
    "evidence/eval-results.json",
    "evidence/PROOF_INDEX.md",
    "evidence/REVIEWER_REVIEW.md",
    "scripts/build_pages.py",
    ".github/workflows/ci.yml",
    ".github/workflows/pages.yml",
]

STAGES = ["SHAPE", "SPECIFY", "DELEGATE", "PROVE", "SHIP", "WATCH"]


def main():
    missing = []
    empty = []
    for item in REQUIRED:
        path = Path(item)
        if not path.exists():
            missing.append(item)
        elif path.is_file() and not path.read_text(encoding="utf-8").strip():
            empty.append(item)

    agents = Path("AGENTS.md").read_text(encoding="utf-8") if Path("AGENTS.md").exists() else ""
    missing_stages = [stage for stage in STAGES if stage not in agents]

    if missing or empty or missing_stages:
        if missing:
            print("Missing:", ", ".join(missing))
        if empty:
            print("Empty:", ", ".join(empty))
        if missing_stages:
            print("Missing Build OS stages in AGENTS.md:", ", ".join(missing_stages))
        raise SystemExit(1)

    print("Build OS contract: PASS")


if __name__ == "__main__":
    main()
