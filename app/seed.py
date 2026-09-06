from datetime import datetime, timedelta, timezone

from .models import TransactionEvent


def card_testing_events() -> list[TransactionEvent]:
    base = datetime(2026, 9, 6, 7, 41, 2, tzinfo=timezone.utc)
    common = {
        "customer_id": "cust_demo_001",
        "account_id": "acct_demo_001",
        "city": "Berlin",
        "country": "DE",
        "device_id": "device_new_999",
        "ip_address": "203.0.113.42",
        "merchant": "Synthetic Merchant",
        "authorized": True,
    }
    amounts = [1.0, 1.0, 2.0, 1.0, 499.0]
    offsets = [0, 6, 12, 19, 27]
    return [
        TransactionEvent(
            event_id=f"evt_{idx+1}",
            transaction_id=f"txn_{idx+1}",
            timestamp=base + timedelta(seconds=offset),
            amount_eur=amount,
            **common,
        )
        for idx, (amount, offset) in enumerate(zip(amounts, offsets))
    ]
