from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from src.schemas.currencies import CurrenciesResponse
from src.schemas.transaction_categories import TransactionCategoriesResponse
from src.schemas.transaction_types import TransactionTypesResponse


class TransactionBase(BaseModel):
    dt_transaction: date = Field(..., description="Transaction's date", le=date.today())
    ds_description: str = Field(..., description="Transaction's description", max_length=200)
    ds_title: str = Field(..., description="Transaction's title", max_length=100)
    vl_transaction: float = Field(..., description="Transaction's value", max_digits=10, decimal_places=2, gt=0)


class TransactionCreate(TransactionBase):
    category_id: int = Field(..., description="Transaction's category id")
    type_id: int = Field(..., description="Transaction's type id")
    currency_id: int = Field(..., description="Transaction's currency")


class TransactionResponse(TransactionBase):
    id: int = Field(..., description="User's database ID")
    ts_created_at: datetime = Field(description="User's creation datetime")
    ts_updated_at: Optional[datetime] = Field(description="User's last update datetime")
    category: TransactionCategoriesResponse = Field(..., description="User's first name")
    type: TransactionTypesResponse = Field(..., description="User's first name")
    currency: CurrenciesResponse = Field(..., description="User's first name")

    model_config = ConfigDict(from_attributes=True)
