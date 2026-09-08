from app.signup_flow import signup_demo_scenarios


def _scenario(name: str):
    return signup_demo_scenarios()["scenarios"][name]


def test_happy_path_and_side_effect_gate():
    scenario = _scenario("happy_path")
    assert scenario["result"]["outcome"] == "COMPLETED"
    assert scenario["result"]["account_status"] == "OPENED"
    assert scenario["result"]["manual_review"] is False


def test_identity_mismatch_blocks_account_opening():
    scenario = _scenario("identity_mismatch")
    assert scenario["result"]["outcome"] == "MANUAL_REVIEW"
    assert scenario["result"]["identity_status"] == "MISMATCH"
    assert scenario["result"]["account_status"] == "NOT_OPENED"
    assert any(item["action"] == "SIDE_EFFECT_BLOCKED" for item in scenario["result"]["audit"])


def test_provider_timeout_is_retryable_and_safe():
    scenario = _scenario("provider_timeout")
    assert scenario["result"]["outcome"] == "RETRY_IDENTITY_PROVIDER"
    assert scenario["result"]["retry_required"] is True
    assert scenario["result"]["account_status"] == "NOT_OPENED"


def test_duplicate_and_out_of_order_events_stay_safe():
    scenario = _scenario("duplicate_out_of_order")
    assert scenario["result"]["outcome"] == "READY_TO_OPEN"
    assert scenario["result"]["account_status"] == "NOT_OPENED"
    actions = [item["action"] for item in scenario["result"]["audit"]]
    assert "IGNORED_DUPLICATE" in actions
    assert "SIDE_EFFECT_BLOCKED" in actions
