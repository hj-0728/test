from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from biz_comprehensive.entity.history.period_category_history import PeriodCategoryHistoryEntity


class PeriodCategoryEntity(VersionedEntity):
    """
    周期类型
    """

    __tablename__ = "st_period_category"
    __table_args__ = {"comment": "周期类型"}
    __history_entity__ = PeriodCategoryHistoryEntity
    name = Column(String(255), comment="周期类型名称", nullable=False)
    code = Column(String(255), comment="编码", nullable=True)
