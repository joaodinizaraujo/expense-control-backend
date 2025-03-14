from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    text,
    ForeignKey,
    Date,
    DECIMAL
)

from src.models.base import Base


class GoalsDB(Base):
    __tablename__ = "tb_goals"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    ds_title = Column(String(100), nullable=False)
    dt_end = Column(Date, nullable=False)
    vl_goal = Column(DECIMAL(10, 2), nullable=False)
    ts_created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    ts_updated_at = Column(TIMESTAMP, nullable=True)

    fk_tb_users_id = Column(Integer, ForeignKey("tb_users.id"), nullable=False)
