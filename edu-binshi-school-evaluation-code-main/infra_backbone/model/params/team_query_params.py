"""
小组
"""
from infra_basic.basic_repository import PageFilterParams


class TeamQueryParams(PageFilterParams):
    team_category_id: str
