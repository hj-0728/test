from infra_utility.token_helper import generate_uuid_id

from domain_evaluation.model.benchmark_calc_node_model import EnumBenchmarkCalcMethod
from domain_evaluation.model.benchmark_execute_node_model import EnumBenchmarkExecuteNodeCategory
from domain_evaluation.model.benchmark_strategy.basic_process_params_type import (
    BasicInputProcessParamsType,
)
from domain_evaluation.model.benchmark_strategy.built_benchmark_node import BuiltBenchmarkNode


class ClassmatesFixedNumberProcessParamsType(BasicInputProcessParamsType):
    classmates_number: int
    stats_method: str

    def to_built_input_node(self, benchmark_id: str, calc_exec_node_id: str) -> BuiltBenchmarkNode:
        input_node = self.dict()
        input_node["benchmark_execute_node_id"] = generate_uuid_id()
        input_node["filler_calc_method"] = "OtherClassmatesBenchmark"
        input_node["filler_calc_context"] = {"classmates_number": self.classmates_number}
        input_exec_node = {
            "id": input_node["benchmark_execute_node_id"],
            "benchmark_id": benchmark_id,
            "name": "同班同学-固定人数_输入",
            "category": EnumBenchmarkExecuteNodeCategory.INPUT.name,
            "next_node_id": calc_exec_node_id,
            "input_node": input_node,
        }
        return BuiltBenchmarkNode(**input_exec_node)

    def to_built_calc_node(self, benchmark_id: str) -> BuiltBenchmarkNode:
        calc_node_id = generate_uuid_id()
        calc_exec_node_id = generate_uuid_id()
        calc_exec_node = {
            "id": calc_exec_node_id,
            "benchmark_id": benchmark_id,
            "name": "同班同学-固定人数_计算",
            "category": EnumBenchmarkExecuteNodeCategory.CALC.name,
            "calc_node": {
                "id": calc_node_id,
                "benchmark_execute_node_id": calc_exec_node_id,
                "input_score_symbol_id": self.score_symbol_id,
                "output_score_symbol_id": self.score_symbol_id,
                "calc_method": EnumBenchmarkCalcMethod.STATS.name,
                "stats_args": {
                    "benchmark_calc_node_id": calc_node_id,
                    "stats_method": self.stats_method,
                },
            },
        }
        return BuiltBenchmarkNode(**calc_exec_node)
