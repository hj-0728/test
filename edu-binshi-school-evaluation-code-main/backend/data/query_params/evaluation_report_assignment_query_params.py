from datetime import datetime
from typing import Optional

from infra_basic.basic_repository import PageFilterParams


class EvaluationReportAssignmentQueryParams(PageFilterParams):
    """
    评价报告的分配 查询条件
    """

    evaluation_criteria_plan_id: str
    dimension_dept_tree_id: Optional[str]
    compared_time: Optional[datetime]

    current_role_code: str
    current_people_id: str
