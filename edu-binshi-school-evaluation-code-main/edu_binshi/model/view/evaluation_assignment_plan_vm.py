from datetime import datetime
from typing import Optional

from infra_basic.basic_model import BasePlusModel


class EvaluationAssignmentPlanViewModel(BasePlusModel):
    evaluation_assignment_id: str
    evaluation_criteria_id: str
    executed_finish_at: datetime
    criteria_name: str
    criteria_comments: Optional[str]
    dept_name: str
    people_name: str
