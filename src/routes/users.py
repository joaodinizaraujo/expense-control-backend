import datetime

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.models.users import UserDB
from src.schemas.amount import AmountResponse
from src.schemas.users import UserCreate, UserResponse, UserUpdate
from src.schemas.users import UserLogin

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
        (UserDB.id_email == user.id_email) | (UserDB.id_cpf == user.id_cpf)
    ).first()

    if existing_user:
        conflict_field = "Email" if existing_user.id_email == user.id_email else "CPF"
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{conflict_field} already registered"
        )

    dict_user = user.model_dump()
    dict_user.pop("ds_password")
    new_user = UserDB(
        **dict_user,
        ds_password=get_password_hash(user.ds_password),
        ts_created_at=datetime.datetime.now(datetime.UTC),
        ts_updated_at=None
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return UserResponse.model_validate(new_user)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database integrity error: {str(exc.detail)}"
        )


@router.patch("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db)
) -> UserResponse:
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

    kwargs = user.model_dump(exclude_unset=True)
    for k, v in kwargs.items():
        if v is not None:
            setattr(db_user, k, v)

    db_user.ts_updated_at = datetime.datetime.now(datetime.UTC)

    try:
        db.commit()
        db.refresh(db_user)
        return UserResponse.model_validate(db_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating user: {str(e)}"
        )


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    existing_user = db.get(UserDB, user_id)
    if existing_user:
        return UserResponse.model_validate(existing_user)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with ID {user_id} not found in database"
    )


@router.get("/amount/{user_id}", response_model=AmountResponse, status_code=status.HTTP_200_OK)
def get_amount_by_id(user_id: int, db: Session = Depends(get_db)) -> AmountResponse:
    existing_user = db.get(UserDB, user_id)
    if existing_user:
        return UserResponse.model_validate(existing_user).amount

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id {user_id} does not have transactions"
    )


@router.post("/login", response_model=UserResponse, status_code=status.HTTP_200_OK)
def login(user: UserLogin, db: Session = Depends(get_db)) -> UserResponse:
    existing_user = db.query(UserDB).filter(UserDB.id_email == user.id_email).first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {user.id_email} not found in database"
        )

    try:
        if not verify_password(user.ds_password, existing_user.ds_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Incorrect password"
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Password may have the incorrect format. Please, change your password"
        )

    return UserResponse.model_validate(existing_user)
