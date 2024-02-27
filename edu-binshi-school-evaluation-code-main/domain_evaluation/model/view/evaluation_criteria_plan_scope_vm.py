from typing import List

from infra_basic.basic_model import BasePlusModel

from domain_evaluation.model.evaluation_criteria_plan_model import EvaluationCriteriaPlanModel
from domain_evaluation.model.evaluation_criteria_plan_scope_model import EvaluationCriteriaPlanScopeModel


class EvaluationCriteriaPlanScopeViewModel(BasePlusModel):
    plan: EvaluationCriteriaPlanModel
    scope_list: List[EvaluationCriteriaPlanScopeModel]
