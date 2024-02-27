from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, Integer, String, Text

from biz_comprehensive.entity.history.indicator_history import IndicatorHistoryEntity


class IndicatorEntity(VersionedEntity):
    """
    指标
    """

    __tablename__ = "st_indicator"
    __table_args__ = {"comment": "指标"}
    __history_entity__ = IndicatorHistoryEntity
    evaluation_criteria_id = Column(String(40), comment="评价标准id", nullable=False)
    parent_id = Column(String(40), comment="父级指标id", nullable=True)
    seq = Column(Integer, comment="排序码", nullable=False)
    name = Column(String(255), comment="名称", nullable=False)
    comment = Column(Text, comment="描述", nullable=True)
    symbol_id = Column(String(40), comment="符号id", nullable=False)
