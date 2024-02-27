from typing import Optional

from infra_utility.algorithm.tree import TreeNodeModel


class DeptTreeViewModel(TreeNodeModel):
    id: str
    name: str
    dept_id: Optional[str]
    parent_dept_id: Optional[str]
    dept_category_code: str
