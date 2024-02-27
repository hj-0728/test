from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import ARRAY, Boolean, Column, Index, Integer, String, text


class ScoreSymbolHistoryEntity(HistoryEntity):
    __tablename__ = "st_score_symbol_history"
    __table_args__ = {"comment": "得分符号（历史）"}

    name = Column(String(255), nullable=False, comment="名称")
    code = Column(String(255), nullable=False, comment="编码")
    value_type = Column(String(255), nullable=False, comment="值类型（枚举num，string）")
    numeric_precision = Column(Integer, nullable=True, comment="精度")
    string_options = Column(ARRAY(String(255)), nullable=True, comment="可选项")
    is_activated = Column(Boolean, nullable=False, comment="是否激活")


Index(
    "idx_score_symbol_history_time_range",
    ScoreSymbolHistoryEntity.id,
    ScoreSymbolHistoryEntity.begin_at,
    ScoreSymbolHistoryEntity.end_at.desc(),
    unique=True,
)
