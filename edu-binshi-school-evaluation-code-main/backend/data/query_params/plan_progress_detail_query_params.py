from typing import Optional

from infra_basic.basic_repository import PageFilterParams


class PlanProgressDetailQueryParams(PageFilterParams):
    """
    计划进展详情
    """

    period_id: Optional[str]
    is_in_progress: Optional[bool]
