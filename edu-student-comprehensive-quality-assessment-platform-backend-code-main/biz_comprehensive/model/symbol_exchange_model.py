from infra_basic.basic_model import VersionedModel


class SymbolExchangeModel(VersionedModel):
    """
    符号兑换
    """

    source_symbol_id: str
    target_symbol_id: str
    exchange_rate: float
