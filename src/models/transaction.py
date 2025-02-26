from src.models.base import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    Date,
    text,
    DECIMAL
)
from sqlalchemy.orm import relationship

class TransactionDB(Base):
    __tablename__ = "tb_transactions"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    dt_transaction = Column(Date, nullable=False)
    ds_description = Column(String(200), nullable=True)
    ds_title = Column(String(100), nullable=False)
    ts_created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    ts_updated_at = Column(TIMESTAMP, nullable=True)
    vl_transaction = Column(DECIMAL(10, 2), nullable=False)
    category = relationship("TransactionCategoriesDB", lazy="joined")
    type = relationship("TransactionTypesDB", lazy="joined")
    currency = relationship("CurrenciesDB", lazy="joined")
