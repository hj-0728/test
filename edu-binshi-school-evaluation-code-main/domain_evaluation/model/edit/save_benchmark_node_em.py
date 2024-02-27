from typing import Dict, Optional

from infra_basic.basic_model import BasePlusModel

from domain_evaluation.model.benchmark_input_node_model import BenchmarkInputNodeModel


class SaveBenchmarkInputNode(BasePlusModel):
    benchmark_id: str
    name: str
    next_node_id: Optional[str]
    seq: int = 1
    input_node: BenchmarkInputNodeModel


class BenchmarkCalcNodeEditModel(BasePlusModel):
    input_score_symbol_id: str
    output_score_symbol_id: str
    calc_method: str
    args: Dict


class SaveBenchmarkCalcNode(BasePlusModel):
    benchmark_id: str
    name: str
    next_node_id: Optional[str]
    calc_node: BenchmarkCalcNodeEditModel
