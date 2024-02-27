from datetime import datetime
from typing import Optional

from infra_basic.basic_model import VersionedModel


class CurrentEvaluationAssignmentViewModel(VersionedModel):
    """
    当前评价分配
    """

    evaluation_criteria_plan_id: str
    effected_category: str
    effected_id: str
    start_at: datetime
    finish_at: Optional[datetime]
    plan_name: str
    focus_period_id: str
    plan_status: str
    executed_start_at: datetime
    executed_finish_at: datetime
    evaluation_criteria_id: str
    evaluation_criteria_name: str
    evaluation_criteria_status: str
    evaluation_object_category: str
    evaluation_object_category_name: Optional[str]
