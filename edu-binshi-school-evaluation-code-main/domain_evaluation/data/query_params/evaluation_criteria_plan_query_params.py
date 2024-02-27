from typing import List, Optional

from infra_basic.basic_repository import PageFilterParams


class EvaluationCriteriaPlanQueryParams(PageFilterParams):
    """
    评价计划 查询条件
    """

    status_list: List[str] = []
    finished: Optional[bool] = None
    is_current_period: Optional[bool] = None
    period_id: Optional[str]
