"""
小组成员
"""
from typing import Optional

from infra_basic.basic_repository import PageFilterParams


class TeamCategoryQueryParams(PageFilterParams):
    is_activated: Optional[str]