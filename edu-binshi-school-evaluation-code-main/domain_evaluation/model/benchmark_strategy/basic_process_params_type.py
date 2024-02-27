from typing import Dict, List, Optional

from infra_basic.basic_model import BasePlusModel

from domain_evaluation.model.benchmark_input_node_model import (
    BenchmarkInputNodeSourceCategory,
    BenchmarkInputNodeSourceExecMode,
)


class BasicInputProcessParamsType(BasePlusModel):
    source_category: str = BenchmarkInputNodeSourceCategory.INPUT.name
    source_benchmark_id: Optional[str]
    source_exec_mode: str = BenchmarkInputNodeSourceExecMode.ONCE.name
    scheduler_expression: Optional[str]
    filler_calc_context: Optional[Dict]
    score_symbol_id: str
    numeric_min_score: Optional[float]
    numeric_max_score: Optional[float]
    limited_string_options: Optional[List[str]]
