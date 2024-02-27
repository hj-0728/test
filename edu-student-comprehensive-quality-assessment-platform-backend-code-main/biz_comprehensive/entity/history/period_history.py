from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, DateTime, Index, String


class PeriodHistoryEntity(HistoryEntity):
    """
    周期历史
    """

    __tablename__ = "st_period_history"
    __table_args__ = {"comment": "周期历史"}
    period_category_id = Column(String(40), comment="周期类型id", nullable=False)
    name = Column(String(255), comment="周期名称", nullable=False)
    code = Column(String(255), comment="编码", nullable=True)
    parent_id = Column(String(40), comment="父级id", nullable=True)
    started_on = Column(DateTime(timezone=True), comment="开始于", nullable=False)
    ended_on = Column(DateTime(timezone=True), comment="结束于", nullable=False)


Index(
    "idx_period_history_time_range",
    PeriodHistoryEntity.id,
    PeriodHistoryEntity.commenced_on,
    PeriodHistoryEntity.ceased_on.desc(),
    unique=True,
)
