from pydantic import BaseModel, Field


class AmountResponse(BaseModel):
    income: float = Field(..., description="User's income")
    outcome: float = Field(..., description="User's outcome")
