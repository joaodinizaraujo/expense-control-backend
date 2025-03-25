import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.models.transactions import TransactionDB
from src.schemas.transactions import TransactionCreate, TransactionResponse

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)) -> TransactionResponse:
    new_transaction = TransactionDB(
        **transaction.model_dump(),
        ts_created_at=datetime.datetime.now(datetime.UTC),
        ts_updated_at=None
    )

    try:
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)
        return TransactionResponse.model_validate(new_transaction)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database integrity error: {str(exc.detail)}"
        )


@router.get("/{transaction_id}", response_model=TransactionResponse, status_code=status.HTTP_200_OK)
def get_transaction_by_id(transaction_id: int, db: Session = Depends(get_db)) -> TransactionResponse:
    existing_transaction = db.get(TransactionDB, transaction_id)
    if existing_transaction:
        return TransactionResponse.model_validate(existing_transaction)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Transaction with ID {transaction_id} not found in database"
    )


@router.get("/user/{user_id}", response_model=list[TransactionResponse], status_code=status.HTTP_200_OK)
def get_transactions_by_user(user_id: int, db: Session = Depends(get_db)) -> list[TransactionResponse]:
    transactions = db.query(TransactionDB).filter(TransactionDB.fk_tb_users_id == user_id)
    if transactions.count() > 0:
        return [TransactionResponse.model_validate(t) for t in transactions]

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id {user_id} does not have transactions"
    )
