from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    Date,
    text,
    DECIMAL, ForeignKey
)
from sqlalchemy.orm import relationship, Mapped

from src.models.base import Base
from src.models.currencies import CurrenciesDB
from src.models.transaction_categories import TransactionCategoriesDB
from src.models.transaction_types import TransactionTypesDB


class TransactionDB(Base):
    __tablename__ = "tb_transactions"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    dt_transaction = Column(Date, nullable=False)
    ds_description = Column(String(200), nullable=True)
    ds_title = Column(String(100), nullable=False)
    ts_created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    ts_updated_at = Column(TIMESTAMP, nullable=True)
    vl_transaction = Column(DECIMAL(10, 2), nullable=False)

    fk_tb_users_id = Column(Integer, ForeignKey("tb_users.id"), nullable=False)
    fk_tb_transaction_categories_id = Column(Integer, ForeignKey("tb_transaction_categories.id"), nullable=False)
    fk_tb_transaction_types_id = Column(Integer, ForeignKey("tb_transaction_types.id"), nullable=False)
    fk_tb_currencies_id = Column(Integer, ForeignKey("tb_currencies.id"), nullable=False)

    category: Mapped[TransactionCategoriesDB] = relationship("TransactionCategoriesDB", lazy="joined")
    type: Mapped[TransactionTypesDB] = relationship("TransactionTypesDB", lazy="joined")
    currency: Mapped[CurrenciesDB] = relationship("CurrenciesDB", lazy="joined")
