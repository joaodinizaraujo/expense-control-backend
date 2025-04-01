from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class TransactionCategoriesBase(BaseModel):
    ds_description: str = Field(..., description="Transaction Category's description", max_length=200)
    ds_title: str = Field(..., description="Transaction Category's title", max_length=100)
    fk_tb_users_id: int = Field(..., description="Transaction Category's creator")


class TransactionCategoriesCreate(TransactionCategoriesBase):
    pass


class TransactionCategoriesResponse(TransactionCategoriesBase):
    id: int = Field(..., description="Transaction Category's database ID")
    ts_created_at: datetime = Field(..., description="Transaction Category's creation datetime")
    ts_updated_at: Optional[datetime] = Field(None, description="Transaction Category's last update datetime")

    model_config = ConfigDict(from_attributes=True)
