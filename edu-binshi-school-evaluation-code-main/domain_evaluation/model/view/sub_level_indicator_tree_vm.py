from typing import Optional

from infra_utility.algorithm.tree import TreeNodeModel


class SubLevelIndicatorTreeItem(TreeNodeModel):
    name: str
    value: str
    parent_id: Optional[str]
    checkable: bool
