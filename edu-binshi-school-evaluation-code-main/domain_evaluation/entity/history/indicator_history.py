from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Boolean, Column, Index, String, Text, text


class IndicatorHistoryEntity(HistoryEntity):
    """
    指标（历史）
    """

    __tablename__ = "st_indicator_history"
    __table_args__ = {"comment": "指标（历史）"}
    name = Column(String(255), comment="名称", nullable=False, index=True)
    comments = Column(Text, comment="描述", nullable=True)
    is_activated = Column(Boolean, nullable=False, comment="是否激活", server_default=text("true"))


Index(
    "idx_indicator_history_time_range",
    IndicatorHistoryEntity.id,
    IndicatorHistoryEntity.begin_at,
    IndicatorHistoryEntity.end_at.desc(),
    unique=True,
)
