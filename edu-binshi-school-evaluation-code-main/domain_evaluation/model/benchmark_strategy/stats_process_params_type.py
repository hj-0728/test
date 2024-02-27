from typing import List, Optional, Dict

from infra_utility.base_plus_model import BasePlusModel
from infra_utility.token_helper import generate_uuid_id

from domain_evaluation.model.benchmark_calc_node_model import EnumBenchmarkCalcMethod, \
    BenchmarkCalcNodeStatsArgsModel, EnumBenchmarkCalcNodeStatsMethod
from domain_evaluation.model.benchmark_execute_node_model import EnumBenchmarkExecuteNodeCategory
from domain_evaluation.model.benchmark_input_node_model import BenchmarkInputNodeSourceCategory
from domain_evaluation.model.benchmark_strategy.built_benchmark_node import \
    BuiltBenchmarkNode, BuiltBenchmarkCalcNode


class StatsProcessParamsType(BasePlusModel):
    score_symbol_id: str
    source_benchmark_id_list: List[str]
    stats_method: str = EnumBenchmarkCalcNodeStatsMethod.SUM.name
    stats_args: Optional[Dict]

    def to_built_calc_node(self, benchmark_id: str) -> BuiltBenchmarkNode:
        exec_calc_node_id = generate_uuid_id()
        calc_node_id = generate_uuid_id()
        return BuiltBenchmarkNode(
            id=exec_calc_node_id,
            benchmark_id=benchmark_id,
            name="统计_计算",
            category=EnumBenchmarkExecuteNodeCategory.CALC.name,
            calc_node=BuiltBenchmarkCalcNode(
                id=calc_node_id,
                benchmark_execute_node_id=exec_calc_node_id,
                input_score_symbol_id=self.score_symbol_id,
                output_score_symbol_id=self.score_symbol_id,
                calc_method=EnumBenchmarkCalcMethod.STATS.name,
                stats_args=BenchmarkCalcNodeStatsArgsModel(
                    benchmark_calc_node_id=calc_node_id,
                    stats_method=self.stats_method,
                    stats_args=self.stats_args,
                )
            )
        )

    def to_built_input_node(
        self, benchmark_id: str, exec_calc_node_id: str
    ) -> List[BuiltBenchmarkNode]:
        input_node_result = []
        for seq, source_benchmark_id in enumerate(self.source_benchmark_id_list):
            exec_input_node_id = generate_uuid_id()
            input_node_id = generate_uuid_id()
            input_exec_node = {
                "id": exec_input_node_id,
                "benchmark_id": benchmark_id,
                "name": "统计_入参",
                "category": EnumBenchmarkExecuteNodeCategory.INPUT.name,
                "seq": seq + 1,
                "next_node_id": exec_calc_node_id,
                "input_node": {
                    "id": input_node_id,
                    "benchmark_execute_node_id": exec_input_node_id,
                    "source_benchmark_id": source_benchmark_id,
                    "source_category": BenchmarkInputNodeSourceCategory.BENCHMARK.name,
                    "filler_calc_method": "StatsBenchmark",
                    "score_symbol_id": self.score_symbol_id,
                },
            }
            input_node_result.append(BuiltBenchmarkNode(**input_exec_node))
        return input_node_result
