from models.agent import Agent
from models.transaction import TransactionRequest


def check_policy(agent: Agent, transaction: TransactionRequest):

    reasons = []

    # Check transaction amount
    if transaction.amount > agent.transaction_limit:
        return {
            "allowed": False,
            "reason": f"Transaction amount ₹{transaction.amount} exceeds "
                       f"the agent limit of ₹{agent.transaction_limit}."
        }

    reasons.append("Transaction amount is within the allowed limit.")

    # Check product category
    if transaction.category not in agent.allowed_categories:
        return {
            "allowed": False,
            "reason": f"Category '{transaction.category}' is not allowed "
                       f"for this agent."
        }

    reasons.append("Product category is allowed.")

    # Check quantity
    if transaction.quantity > 3:
        return {
            "allowed": False,
            "reason": "Quantity exceeds the maximum autonomous purchase limit of 3."
        }

    reasons.append("Quantity is within the allowed limit.")

    return {
        "allowed": True,
        "reasons": reasons
    }