import json
from datetime import datetime


TRANSACTIONS_FILE = "data/transactions.json"


def save_transaction(transaction_data: dict):
    """
    Save a transaction to transaction history.
    """

    # Read existing transactions
    with open(TRANSACTIONS_FILE, "r") as file:
        transactions = json.load(file)

    # Add timestamp
    transaction_data["timestamp"] = datetime.utcnow().isoformat()

    # Add new transaction
    transactions.append(transaction_data)

    # Save updated history
    with open(TRANSACTIONS_FILE, "w") as file:
        json.dump(transactions, file, indent=2)

    return transaction_data


def get_agent_transactions(agent_id: str):
    """
    Return all transactions belonging to an agent.
    """

    with open(TRANSACTIONS_FILE, "r") as file:
        transactions = json.load(file)

    return [
        transaction
        for transaction in transactions
        if transaction["agent_id"] == agent_id
    ]