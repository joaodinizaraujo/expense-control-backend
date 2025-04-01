from pydantic import BaseModel, Field


class AmountResponse(BaseModel):
    amount: float = Field(..., description="User's amount")
