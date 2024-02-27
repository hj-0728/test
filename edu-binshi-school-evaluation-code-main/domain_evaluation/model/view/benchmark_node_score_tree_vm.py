from typing import Optional

from infra_utility.algorithm.tree import TreeNodeModel


class BenchmarkNodeScoreTreeModel(TreeNodeModel):
    """
    基准节点分数树
    """

    id: str
    benchmark_id: str
    category: str
    next_node_id: Optional[str]

    source_score_id: Optional[str]
    source_score_category: Optional[str]

    numeric_score: Optional[float]
    string_score: Optional[str]

    calc_score_log_id: Optional[str]
