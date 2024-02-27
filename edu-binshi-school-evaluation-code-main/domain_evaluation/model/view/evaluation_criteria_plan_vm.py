from datetime import datetime
from typing import Optional

from infra_basic.basic_model import VersionedModel
from infra_utility.base_plus_model import BasePlusModel


class EvaluationCriteriaPlanViewModel(VersionedModel):
    """
    评价标准计划
    """

    evaluation_criteria_id: str
    focus_period_id: str
    name: str
    executed_start_at: datetime
    executed_finish_at: datetime
    status: str
    status_name: Optional[str]
    evaluation_criteria_name: str
    evaluation_criteria_status: str
    evaluation_object_category: str
    report_category: Optional[str]


class EvaluationCriteriaPlanStatsViewModel(BasePlusModel):
    """
    评价标准计划
    """

    evaluation_criteria_plan_id: str
    plan_status: str
    plan_status_name: Optional[str]
    plan_name: str
    executed_start_at: datetime
    executed_finish_at: datetime
    evaluation_criteria_name: str
    evaluation_object_category: str
    evaluation_object_category_name: Optional[str]
    fill_count: int
    not_fill_count: int
    show_report: bool = False
