"""
周期实体类
"""
from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, String

from edu_binshi.entity.history.period_history import PeriodHistoryEntity


class PeriodEntity(VersionedEntity):
    """
    周期
    """

    __tablename__ = "st_period"
    __table_args__ = {"comment": "周期"}
    __history_entity__ = PeriodHistoryEntity
    period_category_id = Column(String(40), comment="周期类型id", nullable=False, index=True)
    name = Column(String(255), comment="名称", nullable=False)
    code = Column(String(255), comment="编码")
    start_at = Column(DateTime(timezone=True), comment="开始于", nullable=False)
    finish_at = Column(DateTime(timezone=True), comment="结束于")
    parent_id = Column(String(40), comment="父级id", index=True)
