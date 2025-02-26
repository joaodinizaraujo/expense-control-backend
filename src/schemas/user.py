from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class UserBase(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    cpf: str = Field(..., description="User's CPF (Brazilian ID)", min_length=11, max_length=11)
    first_name: str = Field(..., description="User's first name", max_length=100)
    last_name: str = Field(..., description="User's last name", max_length=200)
    birthdate: date = Field(..., description="User's birthdate")
    amount: float = Field(description="User's total amount")

    @field_validator("cpf")
    def validate_cpf(cls, v):
        if not re.match(r'^\d{11}$', v):
            raise ValueError("CPF must be 11 digits")
        return v

    @field_validator("amount")
    def validate_amount(cls, v):
        if v < 0:
            raise ValueError("Amount must be higher than 0")
        return v

    @field_validator("birthdate")
    def validate_birthdate(cls, v):
        if v > date.today():
            raise ValueError("Birthdate cannot be in the future")
        return v


class UserCreate(UserBase):
    password: str = Field(..., description="User's password", min_length=8)


class UserResponse(UserBase):
    id: int = Field(..., description="User's database ID")
    created_at: datetime = Field(description="User's creation datetime")
    updated_at: Optional[datetime] = Field(description="User's last update datetime")

    class Config:
        from_attributes = True
