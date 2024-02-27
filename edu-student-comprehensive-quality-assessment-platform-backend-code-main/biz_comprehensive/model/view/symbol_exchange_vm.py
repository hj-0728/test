from infra_basic.basic_model import BasePlusModel


class SymbolExchangeViewModel(BasePlusModel):
    name: str
    code: str
    exchange_rate: float
