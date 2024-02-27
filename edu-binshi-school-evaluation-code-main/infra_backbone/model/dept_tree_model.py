"""
部门树
"""

from datetime import datetime
from typing import Optional

from infra_utility.algorithm.tree import TreeNodeModel


class DeptTreeNodeModel(TreeNodeModel):
    """
    部门树
    """

    id: str
    key: str
    name: str
    level: int
    parent_id: Optional[str]
    parent_name: Optional[str]
    dimension_id: str
    organization_id: str
    dimension_dept_tree_id: Optional[str]
    comments: Optional[str]
    start_at: Optional[datetime]
    finish_at: Optional[datetime]


class DeptTreeModel(TreeNodeModel):
    """
    部门树
    """

    id: str
    key: str
    name: str
    level: int
    parent_id: Optional[str]
    parent_name: Optional[str]
    dimension_dept_tree_id: Optional[str]
    comments: Optional[str]
    dept_category_code: Optional[str]
