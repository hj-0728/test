from typing import Optional, List

from infra_utility.algorithm.tree import TreeNodeModel

from domain_evaluation.model.view.benchmark_input_node_vm import BenchmarkInputNodeVm
from domain_evaluation.model.view.benchmark_vm import BenchmarkSimpleVm


class EvaluationCriteriaTreeViewModel(TreeNodeModel):
    id: str
    name: str
    comments: Optional[str]
    evaluation_criteria_tree_id: Optional[str]
    evaluation_criteria_id: Optional[str]
    evaluation_criteria_name: Optional[str]
    parent_indicator_id: Optional[str]
    parent_id_list: List[str] = []
    level: Optional[int]
    sort_info: List[int] = []
    tag_code: Optional[str]
    benchmark_simple_list: Optional[List[BenchmarkSimpleVm]]
    benchmark_display_list: Optional[List[BenchmarkInputNodeVm]] = []
