from typing import List

from infra_utility.base_plus_model import BasePlusModel
from infra_utility.token_helper import generate_uuid_id

from domain_evaluation.model.benchmark_calc_node_model import EnumBenchmarkCalcMethod
from domain_evaluation.model.benchmark_execute_node_model import EnumBenchmarkExecuteNodeCategory
from domain_evaluation.model.benchmark_input_node_model import BenchmarkInputNodeSourceCategory
from domain_evaluation.model.benchmark_strategy.built_benchmark_node import BuiltBenchmarkNode
from domain_evaluation.model.benchmark_strategy.grade_schema import GradeItemValue


class SourceBenchmarkRangeValue(BasePlusModel):
    min_score: float
    max_score: float
    left_operator: str
    right_operator: str
    match_value: str


class GradeProcessParamsType(BasePlusModel):
    score_symbol_id: str

    sourceBenchmark: GradeItemValue
    range_value_args: List[SourceBenchmarkRangeValue]

    def to_built_calc_node(self, benchmark_id: str) -> BuiltBenchmarkNode:
        exec_calc_node_id = generate_uuid_id()
        calc_node_id = generate_uuid_id()
        range_value_args = [
            {**x.dict(), "benchmark_calc_node_id": calc_node_id} for x in self.range_value_args
        ]
        exec_input_node = {
            "id": exec_calc_node_id,
            "benchmark_id": benchmark_id,
            "name": "区间取值_计算",
            "category": EnumBenchmarkExecuteNodeCategory.CALC.name,
            "calc_node": {
                "id": calc_node_id,
                "benchmark_execute_node_id": exec_calc_node_id,
                "input_score_symbol_id": self.sourceBenchmark.input_score_symbol_id,
                "output_score_symbol_id": self.score_symbol_id,
                "calc_method": EnumBenchmarkCalcMethod.RANGE_VALUE.name,
                "range_value_args": range_value_args,
            },
        }
        return BuiltBenchmarkNode(**exec_input_node)

    def to_built_input_node(self, benchmark_id: str, exec_calc_node_id: str) -> BuiltBenchmarkNode:
        exec_input_node_id = generate_uuid_id()
        exec_input_node = {
            "id": exec_input_node_id,
            "benchmark_id": benchmark_id,
            "name": "区间取值_入参",
            "category": EnumBenchmarkExecuteNodeCategory.INPUT.name,
            "next_node_id": exec_calc_node_id,
            "input_node": {
                "id": generate_uuid_id(),
                "benchmark_execute_node_id": exec_input_node_id,
                "source_benchmark_id": self.sourceBenchmark.source_benchmark_id,
                "source_category": BenchmarkInputNodeSourceCategory.BENCHMARK.name,
                "filler_calc_method": "GradeBenchmark",
                "score_symbol_id": self.sourceBenchmark.input_score_symbol_id,
            },
        }
        return BuiltBenchmarkNode(**exec_input_node)
