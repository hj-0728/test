from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, Numeric, String

from biz_comprehensive.entity.history.symbol_exchange_history import SymbolExchangeHistoryEntity


class SymbolExchangeEntity(VersionedEntity):
    """
    符号兑换
    """

    __tablename__ = "st_symbol_exchange"
    __table_args__ = {"comment": "符号兑换"}
    __history_entity__ = SymbolExchangeHistoryEntity
    source_symbol_id = Column(String(40), comment="源符号id", nullable=False)
    target_symbol_id = Column(String(40), comment="目标符号id", nullable=False)
    exchange_rate = Column(Numeric, comment="兑换比例", nullable=False)
