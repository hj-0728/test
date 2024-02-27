from infra_utility.token_helper import generate_uuid_id

from domain_evaluation.model.benchmark_execute_node_model import EnumBenchmarkExecuteNodeCategory
from domain_evaluation.model.benchmark_strategy.basic_process_params_type import (
    BasicInputProcessParamsType,
)
from domain_evaluation.model.benchmark_strategy.built_benchmark_node import BuiltBenchmarkNode


class InputNoExtraPropertyProcessParamsType(BasicInputProcessParamsType):
    def to_built_input_node(
        self, benchmark_id: str, filler_calc_method: str, name: str
    ) -> BuiltBenchmarkNode:
        input_node = self.dict()
        input_node["benchmark_execute_node_id"] = generate_uuid_id()
        input_node["filler_calc_method"] = filler_calc_method
        input_exec_node = {
            "id": input_node["benchmark_execute_node_id"],
            "benchmark_id": benchmark_id,
            "name": f"{name}_输入",
            "category": EnumBenchmarkExecuteNodeCategory.INPUT.name,
            "input_node": input_node,
        }
        return BuiltBenchmarkNode(**input_exec_node)
