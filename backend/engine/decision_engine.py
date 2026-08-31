def make_decision(risk_score: float):

    if risk_score <= 30:
        return {
            "decision": "APPROVED",
            "reason": "Transaction has low risk."
        }

    elif risk_score <= 70:
        return {
            "decision": "HUMAN_APPROVAL_REQUIRED",
            "reason": "Transaction has medium risk and requires human approval."
        }

    else:
        return {
            "decision": "BLOCKED",
            "reason": "Transaction has high risk."
        }