from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class PeriodCategoryHistoryEntity(HistoryEntity):
    """
    周期类型历史
    """

    __tablename__ = "st_period_category_history"
    __table_args__ = {"comment": "周期类型历史"}
    name = Column(String(255), comment="周期类型名称", nullable=False)
    code = Column(String(255), comment="编码", nullable=True)


Index(
    "idx_period_category_history_time_range",
    PeriodCategoryHistoryEntity.id,
    PeriodCategoryHistoryEntity.commenced_on,
    PeriodCategoryHistoryEntity.ceased_on.desc(),
    unique=True,
)
