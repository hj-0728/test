from typing import List, Optional

from domain_evaluation.model.evaluation_criteria_plan_model import EvaluationCriteriaPlanModel
from domain_evaluation.model.evaluation_criteria_plan_scope_model import ScopeInfo


class EvaluationCriteriaPlanDetailVm(EvaluationCriteriaPlanModel):
    """
    评价标准计划
    """

    period_category_code: str
    scope_category: Optional[str]
    scope_info: Optional[List[ScopeInfo]]
