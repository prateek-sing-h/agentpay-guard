from pydantic import BaseModel, Field


class TransactionRequest(BaseModel):
    agent_id: str
    product: str
    category: str
    amount: float = Field(gt=0)
    quantity: int = Field(gt=0)