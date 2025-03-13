from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from src.schemas.currencies import CurrenciesResponse
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
    id: int = Field(..., description="Transaction's database ID")
    ts_created_at: datetime = Field(description="Transaction's creation datetime")
    ts_updated_at: Optional[datetime] = Field(description="Transaction's last update datetime")
    fk_tb_transaction_categories_id: int = Field(..., description="Transaction's category ID")
    type: TransactionTypesResponse = Field(..., description="Transaction's type")
    currency: CurrenciesResponse = Field(..., description="Transaction's type")

    model_config = ConfigDict(from_attributes=True)
