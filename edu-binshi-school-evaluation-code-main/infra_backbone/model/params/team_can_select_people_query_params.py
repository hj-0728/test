"""
小组成员
"""
from typing import Optional

from infra_basic.basic_repository import PageFilterParams


class TeamCanSelectPeopleQueryParams(PageFilterParams):
    team_id: str
    dimension_category: str
    dimension_dept_tree_id: Optional[str]
