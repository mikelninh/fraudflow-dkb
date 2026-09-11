from analysis.data_tech_lab import COHORT_SIZE, compute_summary, generate_transactions


def test_data_tech_summary_is_deterministic_and_bounded():
    rows_a = generate_transactions()
    rows_b = generate_transactions()
    assert rows_a == rows_b
    assert len(rows_a) == COHORT_SIZE

    summary = compute_summary(rows_a)
    assert summary["synthetic"] is True
    assert summary["transactions"] == COHORT_SIZE
    assert summary["unique_customers"] > 500
    assert 98.0 <= summary["data_quality_pass_rate"] <= 100.0
    assert 1.0 <= summary["alert_rate"] <= 15.0
    assert 0 < summary["confirmed_patterns"] < summary["alerts"]
    assert summary["top_signal"] in {
        "velocity",
        "amount_jump",
        "impossible_travel",
        "new_device_combo",
    }
    assert summary["flow"][-1] == "KPI monitoring"
