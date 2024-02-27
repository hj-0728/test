"""
小组目标树
"""
from typing import Optional

from infra_utility.algorithm.tree import TreeNodeModel


class TeamGoalTreeViwModel(TreeNodeModel):
    """
    小组目标树
    """

    id: str
    key: str
    name: str
    level: int
    parent_id: Optional[str]
    parent_name: Optional[str]
    dimension_dept_tree_id: Optional[str]
    comments: Optional[str]
    dept_category_code: str
    team_name: Optional[str]
    disable_checkbox: Optional[bool] = False
