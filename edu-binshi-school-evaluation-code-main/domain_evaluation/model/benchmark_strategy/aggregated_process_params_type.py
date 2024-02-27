from typing import List

from infra_utility.base_plus_model import BasePlusModel
from infra_utility.token_helper import generate_uuid_id

from domain_evaluation.model.benchmark_calc_node_model import EnumBenchmarkCalcMethod
from domain_evaluation.model.benchmark_execute_node_model import EnumBenchmarkExecuteNodeCategory
from domain_evaluation.model.benchmark_input_node_model import BenchmarkInputNodeSourceCategory
from domain_evaluation.model.benchmark_strategy.built_benchmark_node import BuiltBenchmarkNode


class SourceBenchmarkWeight(BasePlusModel):
    source_benchmark_id: str
    weight: int
    seq: int


class AggregatedProcessParamsType(BasePlusModel):
    score_symbol_id: str
    source_benchmark: List[SourceBenchmarkWeight]

    def to_built_calc_node(self, benchmark_id: str) -> BuiltBenchmarkNode:
        exec_calc_node_id = generate_uuid_id()
        calc_node_id = generate_uuid_id()
        weight_args = []
        for source_benchmark in self.source_benchmark:
            weight_args.append(
                {
                    "benchmark_calc_node_id": calc_node_id,
                    "weight": source_benchmark.weight,
                    "seq": source_benchmark.seq,
                }
            )
        input_exec_node = {
            "id": exec_calc_node_id,
            "benchmark_id": benchmark_id,
            "name": "同一层级分值聚合_计算",
            "category": EnumBenchmarkExecuteNodeCategory.CALC.name,
            "calc_node": {
                "id": calc_node_id,
                "benchmark_execute_node_id": exec_calc_node_id,
                "input_score_symbol_id": self.score_symbol_id,
                "output_score_symbol_id": self.score_symbol_id,
                "calc_method": EnumBenchmarkCalcMethod.WEIGHT.name,
                "weight_args": weight_args,
            },
        }
        return BuiltBenchmarkNode(**input_exec_node)

    def to_built_input_node(
        self, benchmark_id: str, exec_calc_node_id: str
    ) -> List[BuiltBenchmarkNode]:
        input_node_result = []
        for source_benchmark in self.source_benchmark:
            exec_input_node_id = generate_uuid_id()
            input_node_id = generate_uuid_id()
            input_exec_node = {
                "id": exec_input_node_id,
                "benchmark_id": benchmark_id,
                "name": "同一层级分值聚合_入参",
                "category": EnumBenchmarkExecuteNodeCategory.INPUT.name,
                "seq": source_benchmark.seq,
                "next_node_id": exec_calc_node_id,
                "input_node": {
                    "id": input_node_id,
                    "benchmark_execute_node_id": exec_input_node_id,
                    "source_benchmark_id": source_benchmark.source_benchmark_id,
                    "source_category": BenchmarkInputNodeSourceCategory.BENCHMARK.name,
                    "filler_calc_method": "AggregatedBenchmark",
                    "score_symbol_id": self.score_symbol_id,
                },
            }
            input_node_result.append(BuiltBenchmarkNode(**input_exec_node))
        return input_node_result
