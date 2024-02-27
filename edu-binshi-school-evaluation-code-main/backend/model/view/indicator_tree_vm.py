from typing import Optional

from infra_utility.algorithm.tree import TreeNodeModel


class IndicatorTreeVm(TreeNodeModel):
    """
    指标
    """

    id: str
    name: str
    comments: Optional[str]
    parent_indicator_id: Optional[str]
    seq: Optional[int]
