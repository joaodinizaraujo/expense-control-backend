import re
from collections import defaultdict
from datetime import datetime, date
from typing import Optional

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict, computed_field

from src.models.transaction_types import PASSIVE_TYPE_TITLE
from src.schemas.amount import AmountResponse
from src.schemas.category_distribution import CategoryDistributionResponse
from src.schemas.goals import GoalsResponse
from src.schemas.transaction_categories import TransactionCategoriesResponse
from src.schemas.transactions import TransactionResponse


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
    ts_created_at: Optional[datetime] = Field(..., description="User's creation datetime")
    ts_updated_at: Optional[datetime] = Field(description="User's last update datetime")
    transactions: list[TransactionResponse] = Field(..., description="User's transactions")
    categories: list[TransactionCategoriesResponse] = Field(..., description="User's created categories")
    goals: list[GoalsResponse] = Field(..., description="User's goals")

    @computed_field
    @property
    def amount(self) -> AmountResponse:
        if len(self.transactions) > 0:
            return AmountResponse(
                income=sum([
                    t.vl_transaction if t.type.ds_title != PASSIVE_TYPE_TITLE
                    else 0
                    for t in self.transactions
                ]),
                outcome=sum([
                    t.vl_transaction if t.type.ds_title == PASSIVE_TYPE_TITLE
                    else 0
                    for t in self.transactions
                ])
            )

        return AmountResponse(
            income=0.0,
            outcome=0.0
        )

    @computed_field
    @property
    def category_distribution(self) -> CategoryDistributionResponse:
        if len(self.transactions) > 0:
            total = len(self.transactions)
            category_counts = defaultdict(int)
            category_objects = {}

            for t in self.transactions:
                key = id(t.category)
                category_counts[key] += 1
                category_objects[key] = t.category

            categories = []
            percentages = []
            for key, count in category_counts.items():
                categories.append(category_objects[key])
                percentages.append(int((count / total) * 100))

            return CategoryDistributionResponse(
                categories=categories,
                percentages=percentages
            )

        return CategoryDistributionResponse(categories=[], percentages=[])

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    id_email: EmailStr = Field(..., description="User's email address", max_length=100)
    ds_password: str = Field(..., description="User's password", min_length=8, max_length=100)


class UserUpdate(BaseModel):
    id_email: Optional[EmailStr] = Field(None, description="User's email address", max_length=100)
    nm_first_name: Optional[str] = Field(None, description="User's first name", max_length=100)
    nm_last_name: Optional[str] = Field(None, description="User's last name", max_length=200)
