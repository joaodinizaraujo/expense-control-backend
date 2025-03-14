from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.models.transaction_types import TransactionTypesDB
from src.schemas.transaction_types import TransactionTypesResponse

router = APIRouter(
    prefix="/transaction-types",
    tags=["transaction-types"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[TransactionTypesResponse], status_code=status.HTTP_200_OK)
def get_transaction_types(db: Session = Depends(get_db)) -> list[TransactionTypesResponse]:
    types = db.query(TransactionTypesDB).all()
    if types:
        return [TransactionTypesResponse.model_validate(t) for t in types]

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Transaction types not found in database"
    )
