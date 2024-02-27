from typing import List, Optional

from infra_basic.query_params import PageFilterParams


class EvaluationCriteriaPlanStatsQueryParams(PageFilterParams):
    """
    评价标准计划统计  查询条件
    """

    focus_period_id: Optional[str]
    evaluation_object_category_list: List[str] = []
    plan_status_list: List[str] = []
    people_id: Optional[str]
