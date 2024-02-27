from typing import List, Optional

from infra_basic.basic_model import BasePlusModel

from domain_evaluation.model.benchmark_calc_node_model import (
    BenchmarkCalcNodeRangeValueArgsModel,
    BenchmarkCalcNodeStatsArgsModel,
    BenchmarkCalcNodeWeightArgsModel,
)
from domain_evaluation.model.benchmark_input_node_model import BenchmarkInputNodeModel


class BuiltBenchmarkCalcNode(BasePlusModel):
    id: str
    benchmark_execute_node_id: str
    input_score_symbol_id: str
    output_score_symbol_id: str
    calc_method: str

    stats_args: Optional[BenchmarkCalcNodeStatsArgsModel]
    weight_args: Optional[List[BenchmarkCalcNodeWeightArgsModel]]
    range_value_args: Optional[List[BenchmarkCalcNodeRangeValueArgsModel]]


class BuiltBenchmarkNode(BasePlusModel):
    id: str
    benchmark_id: str
    name: str
    category: str
    next_node_id: Optional[str]
    seq: int = 1

    input_node: Optional[BenchmarkInputNodeModel]
    calc_node: Optional[BuiltBenchmarkCalcNode]
