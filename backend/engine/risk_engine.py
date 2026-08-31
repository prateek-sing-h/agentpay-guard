from models.agent import Agent
from models.transaction import TransactionRequest
from engine.velocity_engine import check_velocity


def calculate_risk(
    agent: Agent,
    transaction: TransactionRequest,
    transaction_history: list
):

    risk_score = 0
    reasons = []

    # 1. Agent reputation
    if agent.reputation_score < 50:
        risk_score += 30
        reasons.append("Low agent reputation.")
    elif agent.reputation_score < 75:
        risk_score += 15
        reasons.append("Moderate agent reputation.")
    else:
        risk_score += 5
        reasons.append("High agent reputation.")

    # 2. Transaction amount
    amount_ratio = transaction.amount / agent.transaction_limit

    if amount_ratio >= 0.9:
        risk_score += 25
        reasons.append(
            "Transaction is close to the agent's spending limit."
        )
    elif amount_ratio >= 0.7:
        risk_score += 15
        reasons.append(
            "Transaction amount is relatively high."
        )
    else:
        risk_score += 5
        reasons.append(
            "Transaction amount is relatively low."
        )

    # 3. Quantity
    if transaction.quantity == 3:
        risk_score += 15
        reasons.append(
            "Transaction uses the maximum allowed quantity."
        )
    elif transaction.quantity == 2:
        risk_score += 5
        reasons.append(
            "Transaction quantity is moderate."
        )

    # 4. Transaction velocity
    velocity_result = check_velocity(
        transaction_history,
        transaction.agent_id,
        transaction
    )

    risk_score += velocity_result["velocity_risk"]

    reasons.append(
        velocity_result["reason"]
    )

    # Keep score between 0 and 100
    risk_score = min(risk_score, 100)

    # Determine risk level
    if risk_score <= 30:
        risk_level = "LOW"
    elif risk_score <= 70:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "reasons": reasons
    }