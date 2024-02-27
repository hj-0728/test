from typing import Optional

from infra_utility.algorithm.tree import TreeNodeModel


class AbilityPermissionTreeViewModel(TreeNodeModel):
    """
    功能权限树节点model
    """

    id: str
    version: int
    parent_id: Optional[str]
    name: Optional[str]
    code: Optional[str]
    assigned: Optional[bool]
    node_type: str
    tree_id: str
    tree_version: int
    tree_seq: int
