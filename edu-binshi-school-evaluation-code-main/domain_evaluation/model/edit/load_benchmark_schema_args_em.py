from typing import Optional

from infra_basic.basic_model import BasePlusModel


class LoadBenchmarkSchemaArgsEditModel(BasePlusModel):
    """
    获取基准schema的参数
    """

    strategy_id: str
    indicator_id: Optional[str]
    score_symbol_id: Optional[str]
    benchmark_id: Optional[str]
