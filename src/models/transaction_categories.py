from sqlalchemy.orm import relationship

from src.models.base import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    text,
    ForeignKey
)


class TransactionCategoriesDB(Base):
    __tablename__ = "tb_transaction_categories"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    ds_description = Column(String(200), nullable=True)
    ds_title = Column(String(100), nullable=False)
    ts_created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    ts_updated_at = Column(TIMESTAMP, nullable=True)

    fk_tb_users_id = Column(Integer, ForeignKey("tb_users.id"), nullable=False)
