from pydantic import BaseModel
from src.schemas.transaction_categories import TransactionCategoriesResponse


class CategoryDistributionResponse(BaseModel):
    categories: list[TransactionCategoriesResponse]
    percentages: list[int]
