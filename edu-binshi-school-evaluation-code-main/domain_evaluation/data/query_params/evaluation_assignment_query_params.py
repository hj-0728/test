from typing import List, Optional

from infra_basic.basic_repository import PageFilterParams


class EvaluationAssignmentQueryParams(PageFilterParams):
    """
    评价标准 查询条件
    """

    focus_period_id: Optional[str]
    evaluation_criteria_plan_id: Optional[str]
    evaluation_object_category_list: List[str] = []
    plan_status_list: List[str] = []
    people_id: Optional[str]
