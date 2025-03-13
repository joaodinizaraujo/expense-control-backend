import datetime

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.models.user import UserDB
from src.schemas.user import UserCreate, UserResponse
from src.schemas.user import UserLogin

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    existing_user = db.query(UserDB).filter(
        (UserDB.id_email == user.email) | (UserDB.id_cpf == user.cpf)
    ).first()

    if existing_user:
        conflict_field = "Email" if existing_user.id_email == user.email else "CPF"
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{conflict_field} already registered"
        )

    new_user = UserDB(
        **user.model_dump(),
        vl_amount=0,
        ts_created_at=datetime.datetime.now(datetime.UTC),
        ts_updated_at=None
    )
    validated_user = UserResponse.model_validate(new_user)

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return validated_user
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database integrity error: {str(exc.detail)}"
        )


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    existing_user = db.get(UserDB, user_id)
    if existing_user:
        return UserResponse.model_validate(existing_user)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with the ID {user_id} not found in database"
    )


@router.post("/login", response_model=UserResponse, status_code=status.HTTP_200_OK)
def login(user: UserLogin, db: Session = Depends(get_db)) -> UserResponse:
    existing_user = db.query(UserDB).filter(UserDB.id_email == user.email).first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the email {user.email} not found in database"
        )

    if not verify_password(user.password, existing_user.ds_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Incorrect password"
        )

    return UserResponse.model_validate(existing_user)
