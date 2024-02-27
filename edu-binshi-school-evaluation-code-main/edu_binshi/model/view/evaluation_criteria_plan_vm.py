from datetime import datetime
from typing import Optional

from infra_basic.basic_model import VersionedModel


class EvaluationCriteriaPlanVM(VersionedModel):
    """
    评价标准计划
    """

    evaluation_criteria_id: Optional[str]
    focus_period_id: Optional[str]
    name: Optional[str]
    executed_start_at: Optional[datetime]
    executed_finish_at: Optional[datetime]
    status: Optional[str]
    evaluation_criteria_name: Optional[str]
    report_category: Optional[str]
    period_name: Optional[str]
