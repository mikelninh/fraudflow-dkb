from statistics import mean

from .models import Signal, TransactionEvent


def detect_signals(current: TransactionEvent, history: list[TransactionEvent]) -> list[Signal]:
    signals: list[Signal] = []

    previous_devices = {event.device_id for event in history}
    if history and current.device_id not in previous_devices:
        signals.append(
            Signal(
                name="new_device",
                score=25,
                confidence="HIGH",
                evidence={
                    "device_id": current.device_id,
                    "previous_device_count": len(previous_devices),
                },
            )
        )

    recent = [
        event
        for event in history
        if 0 <= (current.timestamp - event.timestamp).total_seconds() <= 180
    ]
    if len(recent) >= 4:
        window_seconds = int((current.timestamp - recent[0].timestamp).total_seconds())
        signals.append(
            Signal(
                name="transaction_velocity",
                score=35,
                confidence="HIGH",
                evidence={
                    "attempts_in_window": len(recent) + 1,
                    "window_seconds": window_seconds,
                },
            )
        )

    historical_amounts = [event.amount_eur for event in history if event.authorized]
    if historical_amounts:
        baseline = mean(historical_amounts)
        ratio = current.amount_eur / baseline if baseline else 0
        if ratio >= 8:
            signals.append(
                Signal(
                    name="amount_anomaly",
                    score=30,
                    confidence="MEDIUM",
                    evidence={
                        "amount_eur": current.amount_eur,
                        "baseline_mean_eur": round(baseline, 2),
                        "multiple_of_baseline": round(ratio, 1),
                    },
                )
            )

    if history:
        last = history[-1]
        changed_country = current.country != last.country
        seconds = (current.timestamp - last.timestamp).total_seconds()
        if changed_country and 0 <= seconds <= 3600:
            signals.append(
                Signal(
                    name="impossible_travel",
                    score=45,
                    confidence="HIGH",
                    evidence={
                        "from": f"{last.city}, {last.country}",
                        "to": f"{current.city}, {current.country}",
                        "minutes_between": round(seconds / 60, 1),
                    },
                )
            )

    return signals


def risk_score(signals: list[Signal]) -> int:
    return min(100, sum(signal.score for signal in signals))
