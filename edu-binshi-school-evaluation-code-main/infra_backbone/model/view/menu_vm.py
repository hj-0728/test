from typing import List, Optional

from infra_utility.algorithm.tree import TreeNodeModel


class MenuViewModel(TreeNodeModel):
    """
    菜单树
    """

    version: int = 1
    id: Optional[str]
    parent_id: Optional[str]
    name: str
    path: str
    code: Optional[str]
    icon: Optional[str]
    outline: Optional[str]
    open_method: Optional[str]
    permission_id_list: List[str] = []
    permission_name: Optional[str]
