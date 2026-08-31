from pydantic import BaseModel, Field


class Agent(BaseModel):
    agent_id: str
    name: str
    reputation_score: float = Field(ge=0, le=100)
    daily_limit: float = Field(gt=0)
    transaction_limit: float = Field(gt=0)
    allowed_categories: list[str]