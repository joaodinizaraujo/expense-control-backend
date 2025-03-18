from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.models.currencies import CurrenciesDB
from src.schemas.currencies import CurrenciesResponse

router = APIRouter(
    prefix="/currencies",
    tags=["currencies"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[CurrenciesResponse], status_code=status.HTTP_200_OK)
def get_currencies(db: Session = Depends(get_db)) -> list[CurrenciesResponse]:
    types = db.query(CurrenciesDB).all()
    if types:
        return [CurrenciesResponse.model_validate(t) for t in types]

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Currencies not found in database"
    )
