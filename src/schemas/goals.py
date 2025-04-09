from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class GoalsBase(BaseModel):
    ds_title: str = Field(..., description="Goal's title", max_length=100)
    dt_end: date = Field(..., description="Goal's end date", ge=date.today())
    vl_goal: Decimal = Field(..., description="Goal's value", max_digits=10, decimal_places=2, gt=0)


class GoalsCreate(GoalsBase):
    fk_tb_users_id: int = Field(..., description="Goal's user ID")


class GoalsResponse(GoalsBase):
    id: int = Field(..., description="Goal's database ID")
    ts_created_at: datetime = Field(..., description="Goal's creation datetime")
    ts_updated_at: Optional[datetime] = Field(None, description="Goal's last update datetime")

    model_config = ConfigDict(from_attributes=True)