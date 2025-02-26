from src.models.base import Base
from sqlalchemy import (
    Column,
    Integer,
    String
)


class TransactionTypesDB(Base):
    __tablename__ = "tb_transactions"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    ds_title = Column(String(100), nullable=False)
