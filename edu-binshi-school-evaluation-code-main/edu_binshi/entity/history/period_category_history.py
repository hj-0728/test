"""
周期类型历史实体类
"""
from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class PeriodCategoryHistoryEntity(HistoryEntity):
    """
    周期类型（历史实体类）
    """

    __tablename__ = "st_period_category_history"
    __table_args__ = {"comment": "周期类型（历史）"}
    name = Column(String(255), comment="名称", nullable=False)
    code = Column(String(255), comment="编码", nullable=True)


Index(
    "idx_period_category_history_time_range",
    PeriodCategoryHistoryEntity.id,
    PeriodCategoryHistoryEntity.begin_at,
    PeriodCategoryHistoryEntity.end_at.desc(),
    unique=True,
)
