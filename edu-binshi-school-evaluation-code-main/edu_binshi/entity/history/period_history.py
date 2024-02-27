"""
周期历史实体类
"""
from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, DateTime, Index, String


class PeriodHistoryEntity(HistoryEntity):
    """
    周期（历史实体类）
    """

    __tablename__ = "st_period_history"
    __table_args__ = {"comment": "周期（历史）"}
    period_category_id = Column(String(40), comment="周期类型id", nullable=False, index=True)
    name = Column(String(255), comment="名称", nullable=False)
    code = Column(String(255), comment="编码")
    start_at = Column(DateTime(timezone=True), comment="开始于", nullable=False)
    finish_at = Column(DateTime(timezone=True), comment="结束于")
    parent_id = Column(String(40), comment="父级id", index=True)


Index(
    "idx_period_history_time_range",
    PeriodHistoryEntity.id,
    PeriodHistoryEntity.begin_at,
    PeriodHistoryEntity.end_at.desc(),
    unique=True,
)
