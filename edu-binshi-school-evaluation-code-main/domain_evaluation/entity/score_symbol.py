from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import ARRAY, Boolean, Column, Integer, String, text

from domain_evaluation.entity.history.score_symbol_history import ScoreSymbolHistoryEntity


class ScoreSymbolEntity(VersionedEntity):
    __tablename__ = "st_score_symbol"
    __table_args__ = {"comment": "得分符号"}
    __history_entity__ = ScoreSymbolHistoryEntity

    name = Column(String(255), nullable=False, comment="名称")
    code = Column(String(255), nullable=False, comment="编码")
    value_type = Column(String(255), nullable=False, comment="值类型（枚举num，string）")
    numeric_precision = Column(Integer, nullable=True, comment="精度")
    string_options = Column(ARRAY(String(255)), nullable=True, comment="可选项")
    is_activated = Column(
        Boolean, nullable=False, comment="是否激活", default=True, server_default=text("true")
    )
