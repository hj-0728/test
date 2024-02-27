from typing import List, Optional

from infra_utility.algorithm.tree import TreeNodeModel


class DingtalkK12DeptListVm(TreeNodeModel):
    """
    k12部门 vm
    """

    id: Optional[str]
    key: Optional[str]
    name: str
    remarks: Optional[str]
    level: Optional[int]
    parent_id: Optional[str]
    parent_name: Optional[str]
    sort_info: Optional[List[str]]
    parent_list: Optional[List[str]]
    category: Optional[str]
