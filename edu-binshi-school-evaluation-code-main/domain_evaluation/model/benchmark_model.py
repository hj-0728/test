from datetime import datetime
from typing import Dict, Optional

from infra_basic.basic_model import VersionedModel
from infra_utility.base_plus_model import BasePlusModel
from infra_utility.datetime_helper import local_now
from pydantic import Field


class BenchmarkModel(VersionedModel):
    """
    基准
    """

    indicator_id: str
    name: Optional[str]
    guidance: Optional[str]
    start_at: datetime = Field(default_factory=local_now)
    finish_at: Optional[datetime]
    benchmark_strategy_id: str
    benchmark_strategy_params: Dict

    def same_strategy_and_symbol(self, compared_benchmark: "BenchmarkModel") -> bool:
        """
        比较下是否是相同策略下的相同分值符号
        """
        compared_symbol = compared_benchmark.benchmark_strategy_params.get("scoreSymbolId")
        current_symbol = self.benchmark_strategy_params.get("scoreSymbolId")
        if (
            compared_symbol == current_symbol
            and compared_benchmark.benchmark_strategy_id == self.benchmark_strategy_id
        ):
            return True
        return False


class BenchmarkVm(VersionedModel):
    indicator_id: str
    name: str
    guidance: Optional[str]
    start_at: datetime = local_now()
    finish_at: Optional[datetime]
    benchmark_strategy_id: str
    benchmark_strategy_params: Dict
    benchmark_strategy_schema: Optional[BasePlusModel]
    tag_id: Optional[str]

