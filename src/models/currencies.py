from src.models.base import Base
from sqlalchemy import (
    Column,
    Integer,
    String
)


class CurrenciesDB(Base):
    __tablename__ = "tb_transactions"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    cd_iso = Column(String(3), nullable=False)
    ds_title = Column(String(100), nullable=False)
