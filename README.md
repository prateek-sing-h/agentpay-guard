Absolutely. Here is the entire README in one block. Replace everything currently in README.md with this:

# AgentPay Guard

### Trust & Control Layer for Autonomous AI Commerce

AgentPay Guard is a security and decision layer designed for autonomous AI agents that can initiate commerce transactions.

Instead of allowing an AI agent to directly perform a transaction, AgentPay Guard evaluates the request against configurable policies, risk signals, and transaction velocity before making a decision.

## Problem

As AI agents become capable of purchasing products and services autonomously, payment systems need a way to determine:

- Is this agent allowed to make this transaction?
- Is the amount within its spending limit?
- Is the requested category permitted?
- Is the transaction quantity reasonable?
- Is the agent suddenly making too many transactions?
- Should the transaction be approved, blocked, or sent to a human?

AgentPay Guard addresses this control problem.

## Solution

AgentPay Guard places a decision layer between an autonomous agent and a payment action.

```text
AI Agent
   |
   | Transaction Request
   v
+----------------------+
|   AgentPay Guard     |
+----------------------+
          |
          v
+----------------------+
|   Policy Engine      |
+----------------------+
          |
          v
+----------------------+
|    Risk Engine       |
+----------------------+
          |
          v
+----------------------+
| Velocity Detection   |
+----------------------+
          |
          v
+----------------------+
|   Decision Engine    |
+----------------------+
          |
     +----+----+----------------+
     |         |                |
     v         v                v
 APPROVED   HUMAN REVIEW     BLOCKED
Core Features
1. Policy Enforcement

Every transaction is checked against agent-level policies such as:

Maximum transaction amount
Allowed product categories
Maximum quantity

Example:

Agent limit: ₹10,000
Requested amount: ₹15,000

Result: BLOCKED
Reason: Transaction exceeds agent spending limit.
2. Risk Scoring

Transactions that pass basic policy checks are evaluated using multiple risk signals.

Current signals include:

Agent reputation
Transaction amount
Transaction quantity
Transaction velocity

The system produces:

Risk score
Risk level
Risk reasons
Explainable decision reason
3. Transaction Velocity Detection

AgentPay Guard monitors recent transaction activity.

If an agent attempts an unusually high number of transactions within a short period, the risk level increases and the system can require human approval.

Example:

Agent activity:
7+ transactions within one minute

Result:
Elevated risk
→ HUMAN_APPROVAL_REQUIRED
4. Explainable Decisions

The system does not simply return a decision.

It explains why the transaction was:

APPROVED
HUMAN_APPROVAL_REQUIRED
BLOCKED

Example:

{
  "decision": "APPROVED",
  "risk_score": 15,
  "risk_level": "LOW",
  "decision_reason": "Transaction has low risk.",
  "risk_reasons": [
    "High agent reputation.",
    "Transaction amount is relatively low.",
    "Transaction quantity is moderate.",
    "Transaction frequency is within normal limits."
  ]
}
5. Transaction History

Transactions are persisted locally and used to evaluate recent agent behavior and transaction frequency.

6. Transaction Simulation

The system can generate batches of synthetic transactions for testing.

Example:

POST /simulate?count=10

The simulator produces different outcomes including:

APPROVED
HUMAN_APPROVAL_REQUIRED
BLOCKED
API

AgentPay Guard is built using FastAPI.

Health Check
GET /health
Evaluate Transaction
POST /evaluate-transaction

Example:

{
  "agent_id": "agent_001",
  "product": "Wireless Headphones",
  "category": "Electronics",
  "amount": 6000,
  "quantity": 2
}

Possible result:

APPROVED
Intent Parsing
POST /parse-intent

Example request:

Buy 2 wireless headphones for ₹6000

The intent layer converts the request into structured transaction information.

Example output:

{
  "product": "Wireless Headphones",
  "category": "Electronics",
  "amount": 6000,
  "quantity": 2
}
Transaction Simulation
POST /simulate?count=10

Generates and evaluates multiple synthetic transactions.

Example Decisions
Approved
Amount: ₹6,000
Category: Electronics
Quantity: 2
Risk Score: 15
Risk Level: LOW

→ APPROVED
Blocked
Amount: ₹15,000
Agent Limit: ₹10,000

→ BLOCKED
Human Approval
Transaction frequency becomes unusually high.

Risk Level: MEDIUM

→ HUMAN_APPROVAL_REQUIRED
Architecture
agentpay-guard/
│
├── backend/
│   │
│   ├── main.py
│   │
│   ├── engine/
│   │   ├── policy_engine.py
│   │   ├── risk_engine.py
│   │   ├── velocity_engine.py
│   │   └── decision_engine.py
│   │
│   ├── models/
│   │   ├── agent.py
│   │   └── transaction.py
│   │
│   ├── services/
│   │   ├── ai_service.py
│   │   ├── simulation_service.py
│   │   └── transaction_service.py
│   │
│   └── data/
│       ├── agents.json
│       └── transactions.json
│
├── .gitignore
├── README.md
└── requirements.txt
Technology Stack
Python
FastAPI
Pydantic
Uvicorn
Rule-based policy and risk evaluation
JSON-based transaction persistence
Synthetic transaction simulation
Natural-language transaction intent parsing
Running Locally

Clone the repository:

git clone https://github.com/prateek-sing-h/agentpay-guard.git
cd agentpay-guard

Create a virtual environment:

python -m venv backend/venv

Windows:

backend\venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Start the API:

cd backend
uvicorn main:app --reload

Open the interactive API documentation:

http://127.0.0.1:8000/docs
Example Flow

A natural-language request can be converted into a structured transaction:

"Buy 2 wireless headphones for ₹6000"
                |
                v
        Intent Parsing
                |
                v
Product: Wireless Headphones
Category: Electronics
Amount: ₹6000
Quantity: 2
                |
                v
          Policy Check
                |
                v
           Risk Check
                |
                v
      Velocity Detection
                |
                v
       Decision Engine
                |
       +--------+--------+
       |        |        |
       v        v        v
   APPROVED   HUMAN    BLOCKED
              REVIEW
Design Principle

AgentPay Guard follows a simple principle:

An autonomous agent should not receive unrestricted authority to spend money.

Every transaction should be:

Bounded → Evaluated → Explainable → Auditable

The system separates policy enforcement from risk evaluation and final decision-making so that payment actions can be controlled before execution.

Current Status

This project is an MVP/prototype built for the Razorpay AI Builder Buildathon.

Current implementation demonstrates:

Policy-based transaction control
Risk scoring
Velocity detection
Explainable decisions
Human approval escalation
Transaction history
Synthetic transaction simulation
Natural-language transaction intent parsing
FastAPI-based transaction evaluation APIs
Future Direction

Potential production extensions include:

Razorpay Test Mode payment execution
Stronger AI/LLM-based intent extraction
Merchant-specific policies
Agent identity and reputation
Persistent database storage
Human approval dashboard
Production-grade audit logs
Advanced behavioral risk models
Author

Prateek Singh

Built for the Razorpay AI Builder Internship 2026.