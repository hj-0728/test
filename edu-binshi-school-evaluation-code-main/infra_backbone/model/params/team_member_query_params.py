"""
小组成员
"""
from infra_basic.basic_repository import PageFilterParams


class TeamMemberQueryParams(PageFilterParams):
    team_id: str
