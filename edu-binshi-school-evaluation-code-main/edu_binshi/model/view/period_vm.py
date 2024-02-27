from datetime import datetime
from typing import List, Optional

from infra_utility.algorithm.tree import TreeNodeModel


class PeriodTreeNodeVm(TreeNodeModel):
    """
    周期树
    """

    id: str
    period_category_id: str
    name: str
    start_at: datetime
    finish_at: datetime
    parent_id: Optional[str]
    seq: Optional[int]
    path_ids: List[str]
    category_name: str
    category_code: str
