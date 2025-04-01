import datetime
from sqlite3 import IntegrityError

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.models.transaction_categories import TransactionCategoriesDB
from src.schemas.transaction_categories import TransactionCategoriesCreate, TransactionCategoriesResponse

router = APIRouter(
    prefix="/transaction-categories",
    tags=["transaction-categories"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/{transaction_category_id}", 
    response_model=TransactionCategoriesResponse, 
    status_code=status.HTTP_200_OK
)
def get_transaction_category_by_id(
    transaction_category_id: int, 
    db: Session = Depends(get_db)
) -> TransactionCategoriesResponse:
    existing_category = db.get(TransactionCategoriesDB, transaction_category_id)
    if existing_category:
        return TransactionCategoriesResponse.model_validate(existing_category)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Transaction category with ID {transaction_category_id} not found in database"
    )


@router.post("/", response_model=TransactionCategoriesResponse, status_code=status.HTTP_201_CREATED)
def create_transaction_category(
    transaction_category: TransactionCategoriesCreate,
    db: Session = Depends(get_db)
) -> TransactionCategoriesResponse:
    dict_transaction_categories = transaction_category.model_dump()
    new_transaction_categories = TransactionCategoriesDB(
        **dict_transaction_categories,
        ts_created_at=datetime.datetime.now(datetime.UTC),
        ts_updated_at=None
    )

    try:
        db.add(new_transaction_categories)
        db.commit()
        db.refresh(new_transaction_categories)
        return TransactionCategoriesResponse.model_validate(new_transaction_categories)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database integrity error: {str(exc.detail)}"
        )
