from src.models.base import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    text
)


class CurrenciesDB(Base):
    __tablename__ = "tb_currencies"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    cd_iso = Column(String(3), nullable=False)
    ds_title = Column(String(100), nullable=False)
    ts_created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    ts_updated_at = Column(TIMESTAMP, nullable=True)
