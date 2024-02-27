from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Boolean, Column, String, Text, text

from domain_evaluation.entity.history.indicator_history import IndicatorHistoryEntity


class IndicatorEntity(VersionedEntity):
    """
    指标
    """

    __tablename__ = "st_indicator"
    __table_args__ = {"comment": "指标"}
    __history_entity__ = IndicatorHistoryEntity
    name = Column(String(255), comment="名称", nullable=False, index=True)
    comments = Column(Text, comment="描述", nullable=True)
    is_activated = Column(Boolean, nullable=False, comment="是否激活", server_default=text("true"))
