import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
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
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def db_to_response(user: UserDB) -> UserResponse:
    return UserResponse(
        id=user.id,
        email=user.id_email,
        cpf=user.id_cpf,
        birthdate=user.dt_birthdate,
        first_name=user.nm_first_name,
        last_name=user.nm_last_name,
        created_at=user.ts_created_at,
        updated_at=user.ts_updated_at,
        amount=user.vl_amount
    )


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


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
        id_email=user.email,
        id_cpf=user.cpf,
        dt_birthdate=user.birthdate,
        nm_first_name=user.first_name,
        nm_last_name=user.last_name,
        ds_password=get_password_hash(user.password),
        vl_amount=0,
        ts_created_at=datetime.datetime.now(datetime.UTC),
        ts_updated_at=None
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return db_to_response(new_user)
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
        return db_to_response(existing_user)

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

    if not verify_password(user.password, existing_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Incorrect password"
        )

    return db_to_response(existing_user)
