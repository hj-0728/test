from datetime import datetime
from typing import List, Optional

from infra_utility.algorithm.tree import TreeNodeModel

from domain_evaluation.model.evaluation_criteria_tree_model import BenchmarkListItemVm


class EvaluationCriteriaTreeNodeModel(TreeNodeModel):
    """
    评价标准的树（对用户可以叫评价项） model
    """

    evaluation_criteria_id: str
    id: str
    version: int
    key: str
    name: str
    level: int
    parent_indicator_id: Optional[str]
    indicator_id: Optional[str]
    tag: Optional[str]
    comments: Optional[str]
    indicator_version: Optional[int]
    seq: int
    is_activated: bool = True
    start_at: Optional[datetime]
    finish_at: Optional[datetime]
    benchmark_list: Optional[List[BenchmarkListItemVm]]
