from __future__ import annotations

import random
import sqlite3
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone

SEED = 20260911
COHORT_SIZE = 5000


@dataclass(frozen=True)
class SyntheticTransaction:
    transaction_id: str
    customer_id: str
    timestamp: str
    amount_eur: float
    country: str
    device_id: str
    data_complete: int
    alert_reason: str
    analyst_outcome: str


def generate_transactions(size: int = COHORT_SIZE, seed: int = SEED) -> list[SyntheticTransaction]:
    """Generate a deterministic synthetic transaction cohort for analytics proof only."""
    rng = random.Random(seed)
    start = datetime(2026, 1, 15, 8, 0, tzinfo=timezone.utc)
    countries = ["DE", "DE", "DE", "DE", "AT", "NL", "FR"]
    rows: list[SyntheticTransaction] = []

    for index in range(size):
        customer_id = f"C-{rng.randrange(1, 801):04d}"
        transaction_id = f"T-{index + 1:05d}"
        timestamp = start + timedelta(seconds=index * 17 + rng.randrange(0, 13))
        amount = round(max(0.5, rng.lognormvariate(2.4, 1.0)), 2)
        country = rng.choice(countries)
        device_id = f"D-{rng.randrange(1, 1201):04d}"
        data_complete = 0 if rng.random() < 0.006 else 1

        velocity = rng.random() < 0.035
        amount_jump = amount > 240 and rng.random() < 0.55
        impossible_travel = country != "DE" and rng.random() < 0.035
        new_device_combo = rng.random() < 0.018 and amount > 120

        reasons = []
        if velocity:
            reasons.append("velocity")
        if amount_jump:
            reasons.append("amount_jump")
        if impossible_travel:
            reasons.append("impossible_travel")
        if new_device_combo:
            reasons.append("new_device_combo")

        if not data_complete:
            alert_reason = "data_quality"
            analyst_outcome = "REVIEW_DATA"
        elif reasons:
            alert_reason = "+".join(reasons)
            analyst_outcome = "CONFIRMED_PATTERN" if rng.random() < 0.32 else "CLEARED"
        else:
            alert_reason = "none"
            analyst_outcome = "NO_ALERT"

        rows.append(
            SyntheticTransaction(
                transaction_id=transaction_id,
                customer_id=customer_id,
                timestamp=timestamp.isoformat(),
                amount_eur=amount,
                country=country,
                device_id=device_id,
                data_complete=data_complete,
                alert_reason=alert_reason,
                analyst_outcome=analyst_outcome,
            )
        )

    return rows


def build_database(rows: list[SyntheticTransaction]) -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute(
        """
        CREATE TABLE transactions (
            transaction_id TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            amount_eur REAL NOT NULL,
            country TEXT NOT NULL,
            device_id TEXT NOT NULL,
            data_complete INTEGER NOT NULL,
            alert_reason TEXT NOT NULL,
            analyst_outcome TEXT NOT NULL
        )
        """
    )
    conn.executemany(
        """
        INSERT INTO transactions (
            transaction_id, customer_id, timestamp, amount_eur, country,
            device_id, data_complete, alert_reason, analyst_outcome
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [tuple(asdict(row).values()) for row in rows],
    )
    return conn


def compute_summary(rows: list[SyntheticTransaction] | None = None) -> dict:
    rows = rows or generate_transactions()
    conn = build_database(rows)

    total = conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
    complete = conn.execute("SELECT COUNT(*) FROM transactions WHERE data_complete = 1").fetchone()[0]
    alerts = conn.execute(
        "SELECT COUNT(*) FROM transactions WHERE alert_reason NOT IN ('none', 'data_quality')"
    ).fetchone()[0]
    confirmed = conn.execute(
        "SELECT COUNT(*) FROM transactions WHERE analyst_outcome = 'CONFIRMED_PATTERN'"
    ).fetchone()[0]
    customers = conn.execute("SELECT COUNT(DISTINCT customer_id) FROM transactions").fetchone()[0]

    reason_counter: Counter[str] = Counter()
    for row in rows:
        if row.alert_reason in {"none", "data_quality"}:
            continue
        for reason in row.alert_reason.split("+"):
            reason_counter[reason] += 1

    top_reason, top_reason_count = reason_counter.most_common(1)[0]

    return {
        "synthetic": True,
        "seed": SEED,
        "transactions": total,
        "unique_customers": customers,
        "data_quality_pass_rate": round(complete / total * 100, 1),
        "alerts": alerts,
        "alert_rate": round(alerts / total * 100, 1),
        "confirmed_patterns": confirmed,
        "top_signal": top_reason,
        "top_signal_count": top_reason_count,
        "flow": [
            "Source events",
            "Data quality gate",
            "Typed model",
            "Fraud signals",
            "Human review",
            "KPI monitoring",
        ],
        "boundaries": [
            "synthetic cohort only",
            "no production fraud model",
            "no fabricated model accuracy",
            "human review remains authoritative",
        ],
    }


if __name__ == "__main__":
    import json

    print(json.dumps(compute_summary(), indent=2))
