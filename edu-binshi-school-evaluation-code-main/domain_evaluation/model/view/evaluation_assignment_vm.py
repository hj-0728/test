from datetime import datetime
from typing import Optional

from infra_basic.basic_model import BasicModel


class EvaluationAssignmentViewModel(BasicModel):
    evaluation_criteria_plan_id: str
    plan_name: str
    plan_status: str
    plan_status_name: Optional[str]
    executed_start_at: datetime
    executed_finish_at: datetime
    evaluation_criteria_id: str
    evaluation_criteria_name: str
    evaluation_object_category: str
    evaluation_object_category_name: Optional[str]
    avatar_bucket_name: Optional[str]
    avatar_object_name: Optional[str]
    avatar_url: Optional[str]
    people_name: str
    dept_name: str
    effected_name: str
    fill_count: int
    not_fill_count: int
    show_report: bool = False
