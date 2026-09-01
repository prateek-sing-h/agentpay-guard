from fastapi import FastAPI, HTTPException
import json

from models.agent import Agent
from models.transaction import TransactionRequest
from engine.policy_engine import check_policy
from engine.risk_engine import calculate_risk
from engine.decision_engine import make_decision
from services.transaction_service import save_transaction
from services.transaction_service import get_agent_transactions
from services.simulation_service import generate_transaction
from services.ai_service import parse_intent


app = FastAPI(
    title="AgentPay Guard",
    description="Trust and control layer for autonomous AI commerce",
    version="1.0.0"
)


# Load agent data from JSON file
with open("data/agents.json", "r") as file:
    agent_data = json.load(file)


# Convert JSON data into Agent objects
agents = {
    agent["agent_id"]: Agent(**agent)
    for agent in agent_data
}


@app.get("/")
def root():
    return {
        "project": "AgentPay Guard",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/evaluate-transaction")
def evaluate_transaction(transaction: TransactionRequest):

    # Find the AI agent
    agent = agents.get(transaction.agent_id)

    if not agent:
        raise HTTPException(
            status_code=404,
            detail="Agent not found"
        )

    # Check merchant/agent policies
    policy_result = check_policy(agent, transaction)

    # If policy fails, block the transaction
    if not policy_result["allowed"]:

        result = {
            "decision": "BLOCKED",
            "agent_id": transaction.agent_id,
            "risk_score": None,
            "risk_level": None,
            "decision_reason": policy_result["reason"],
            "policy_reasons": [
                policy_result["reason"]
            ],
            "risk_reasons": []
        }

        # Save blocked transaction
        save_transaction({
            **transaction.model_dump(),
            **result
        })

        return result

    transaction_history = get_agent_transactions(
    transaction.agent_id
)

    risk_result = calculate_risk(
    agent,
    transaction,
    transaction_history
)

    # Make final decision
    decision_result = make_decision(
        risk_result["risk_score"]
    )

    result = {
        "decision": decision_result["decision"],
        "agent_id": transaction.agent_id,
        "risk_score": risk_result["risk_score"],
        "risk_level": risk_result["risk_level"],
        "decision_reason": decision_result["reason"],
        "policy_reasons": policy_result["reasons"],
        "risk_reasons": risk_result["reasons"]
    }

    # Save transaction history
    save_transaction({
        **transaction.model_dump(),
        **result
    })

    return result

@app.post("/simulate")
def simulate_transactions(count: int = 10):

    results = []

    for _ in range(count):

        transaction_data = generate_transaction("agent_001")

        transaction = TransactionRequest(**transaction_data)

        result = evaluate_transaction(transaction)

        results.append(result)

    return {
        "total_transactions": count,
        "results": results
    }

@app.post("/parse-intent")
def parse_user_intent(text: str):

    intent = parse_intent(text)

    if intent["product"] == "Unknown":
        raise HTTPException(
            status_code=400,
            detail="Could not identify the product."
        )

    if intent["amount"] is None:
        raise HTTPException(
            status_code=400,
            detail="Could not identify the amount."
        )

    return intent