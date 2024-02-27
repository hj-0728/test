from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, Integer, String, Text


class IndicatorHistoryEntity(HistoryEntity):
    """
    指标历史
    """

    __tablename__ = "st_indicator_history"
    __table_args__ = {"comment": "指标历史"}
    evaluation_criteria_id = Column(String(40), comment="评价标准id", nullable=False)
    parent_id = Column(String(40), comment="父级指标id", nullable=True)
    seq = Column(Integer, comment="排序码", nullable=False)
    name = Column(String(255), comment="名称", nullable=False)
    comment = Column(Text, comment="描述", nullable=True)
    symbol_id = Column(String(40), comment="符号id", nullable=False)


Index(
    "idx_indicator_history_time_range",
    IndicatorHistoryEntity.id,
    IndicatorHistoryEntity.commenced_on,
    IndicatorHistoryEntity.ceased_on.desc(),
    unique=True,
)
