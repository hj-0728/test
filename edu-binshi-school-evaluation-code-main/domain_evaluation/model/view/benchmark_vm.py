from typing import Optional

from infra_utility.base_plus_model import BasePlusModel


class BenchmarkSimpleVm(BasePlusModel):
    benchmark_id: str
    benchmark_name: str
    score_symbol_name: str
    score_symbol_code: str
    score_result: Optional[str]
    benchmark_source_category: Optional[str]
