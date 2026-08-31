from datetime import datetime, timedelta


def check_velocity(transactions, agent_id, current_transaction):

    now = datetime.utcnow()

    recent_transactions = []

    for transaction in transactions:

        if transaction["agent_id"] != agent_id:
            continue

        timestamp = datetime.fromisoformat(
            transaction["timestamp"]
        )

        if now - timestamp <= timedelta(minutes=1):
            recent_transactions.append(transaction)

    transaction_count = len(recent_transactions)

    # Include the current transaction
    transaction_count += 1

    if transaction_count >= 10:
        return {
            "velocity_risk": 30,
            "velocity_level": "HIGH",
            "reason": (
                f"Agent has attempted {transaction_count} "
                "transactions within the last minute."
            )
        }

    elif transaction_count >= 5:
        return {
            "velocity_risk": 15,
            "velocity_level": "MEDIUM",
            "reason": (
                f"Agent has attempted {transaction_count} "
                "transactions within the last minute."
            )
        }

    return {
        "velocity_risk": 0,
        "velocity_level": "LOW",
        "reason": "Transaction frequency is within normal limits."
    }