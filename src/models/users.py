from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    Date,
    text,
    DECIMAL
)
from sqlalchemy.orm import relationship, Mapped

from src.models.base import Base
from src.models.goals import GoalsDB
from src.models.transactions import TransactionDB
from src.models.transaction_categories import TransactionCategoriesDB


class UserDB(Base):
    __tablename__ = "tb_users"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    id_email = Column(String(100), nullable=False, unique=True)
    id_cpf = Column(String(11), nullable=False, unique=True)
    dt_birthdate = Column(Date, nullable=False)
    nm_first_name = Column(String(100), nullable=False)
    nm_last_name = Column(String(200), nullable=False)
    ds_password = Column(String(100), nullable=False)
    ts_created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    ts_updated_at = Column(TIMESTAMP, nullable=True)
    vl_amount = Column(DECIMAL(10, 2), server_default=text("0.00"), nullable=False)

    transactions: Mapped[list[TransactionDB]] = relationship("TransactionDB", lazy="joined")
    categories: Mapped[list[TransactionCategoriesDB]] = relationship("TransactionCategoriesDB", lazy="joined")
    goals: Mapped[list[GoalsDB]] = relationship("GoalsDB", lazy="joined")
