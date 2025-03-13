import re
from datetime import datetime, date
from typing import Optional

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict

from src.schemas.transaction import TransactionResponse
from src.schemas.transaction_categories import TransactionCategoriesResponse


class UserBase(BaseModel):
    id_email: EmailStr = Field(..., description="User's email address", max_length=100)
    id_cpf: str = Field(..., description="User's CPF (Brazilian ID)", min_length=11, max_length=11)
    nm_first_name: str = Field(..., description="User's first name", max_length=100)
    nm_last_name: str = Field(..., description="User's last name", max_length=200)
    dt_birthdate: date = Field(..., description="User's birthdate")

    @field_validator("id_cpf")
    def validate_cpf(cls, v):
        if not re.match(r'^\d{11}$', v):
            raise ValueError("CPF must be 11 digits")
        return v

    @field_validator("dt_birthdate")
    def validate_birthdate(cls, v):
        if v > date.today() - relativedelta(years=14):
            raise ValueError(f"you must be at least 14 years old")

        return v


class UserCreate(UserBase):
    ds_password: str = Field(..., description="User's password", min_length=8, max_length=100)


class UserResponse(UserBase):
    id: int = Field(..., description="User's database ID")
    ts_created_at: Optional[datetime] = Field(description="User's creation datetime")
    ts_updated_at: Optional[datetime] = Field(description="User's last update datetime")
    vl_amount: Optional[float] = Field(description="User's total amount")
    transactions: list[TransactionResponse] = Field(description="User's transactions")
    categories: list[TransactionCategoriesResponse] = Field(description="User's created categories")

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    id_email: EmailStr = Field(..., description="User's email address", max_length=100)
    ds_password: str = Field(..., description="User's password", min_length=8, max_length=100)
