from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class TransactionTypesBase(BaseModel):
    ds_title: str = Field(..., description="Transaction Type's title", max_length=100)


class TransactionTypesCreate(TransactionTypesBase):
    pass


class TransactionTypesResponse(TransactionTypesBase):
    id: int = Field(..., description="Transaction Type's database ID")
    ts_created_at: datetime = Field(..., description="Transaction Type's creation datetime")
    ts_updated_at: Optional[datetime] = Field(None, description="Transaction Type's last update datetime")

    model_config = ConfigDict(from_attributes=True)
