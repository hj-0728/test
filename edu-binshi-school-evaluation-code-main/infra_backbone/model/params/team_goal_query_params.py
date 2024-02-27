"""
小组成员
"""
from typing import Optional

from infra_basic.basic_repository import PageFilterParams


class TeamGoalQueryParams(PageFilterParams):
    team_id: Optional[str]
    team_category_id: str
