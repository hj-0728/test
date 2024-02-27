from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, Numeric, String


class SymbolExchangeHistoryEntity(HistoryEntity):
    """
    符号兑换历史
    """

    __tablename__ = "st_symbol_exchange_history"
    __table_args__ = {"comment": "符号兑换历史"}
    source_symbol_id = Column(String(40), comment="源符号id", nullable=False)
    target_symbol_id = Column(String(40), comment="目标符号id", nullable=False)
    exchange_rate = Column(Numeric, comment="兑换比例", nullable=False)


Index(
    "idx_symbol_exchange_history_time_range",
    SymbolExchangeHistoryEntity.id,
    SymbolExchangeHistoryEntity.commenced_on,
    SymbolExchangeHistoryEntity.ceased_on.desc(),
    unique=True,
)
