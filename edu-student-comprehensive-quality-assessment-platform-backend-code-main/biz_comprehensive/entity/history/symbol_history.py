from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import ARRAY, Boolean, Column, Index, Integer, String


class SymbolHistoryEntity(HistoryEntity):
    """
    符号历史
    """

    __tablename__ = "st_symbol_history"
    __table_args__ = {"comment": "符号历史"}
    name = Column(String(255), comment="名称", nullable=False)
    code = Column(String(255), comment="编码", nullable=True)
    value_type = Column(String(255), comment="值类型（枚举num，string）（NUM.STRING）", nullable=False)
    numeric_precision = Column(Integer, comment="数值精度", nullable=True)
    string_options = Column(ARRAY(String(255)), comment="字符串选项", nullable=True)
    is_activated = Column(Boolean, comment="是否激活", nullable=False)
    category = Column(
        String(255),
        comment="类别（积分/闪光点/闪光点展示/得分, POINTS/BRIGHT_SPOT/BRIGHT_SPOT_SHOW/SCORE）",
        nullable=False,
    )


Index(
    "idx_symbol_history_time_range",
    SymbolHistoryEntity.id,
    SymbolHistoryEntity.commenced_on,
    SymbolHistoryEntity.ceased_on.desc(),
    unique=True,
)
