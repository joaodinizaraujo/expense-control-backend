from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class CurrenciesBase(BaseModel):
    cd_iso: str = Field(
        ...,
        description="Currency's iso code, Example: USD, EUR, BRL",
        min_length=3,
        max_length=3
    )
    ds_title: str = Field(..., description="Currency's title", max_length=100)


class CurrenciesCreate(CurrenciesBase):
    pass


class CurrenciesResponse(CurrenciesBase):
    id: int = Field(..., description="Currency's database ID")
    ts_created_at: datetime = Field(..., description="Currency's creation datetime")
    ts_updated_at: Optional[datetime] = Field(None, description="Currency's last update datetime")

    model_config = ConfigDict(from_attributes=True)
