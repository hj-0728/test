from datetime import datetime
from enum import Enum
from typing import Optional, List

from infra_basic.basic_model import VersionedModel
from infra_utility.base_plus_model import BasePlusModel

from domain_evaluation.model.evaluation_criteria_plan_model import EvaluationCriteriaPlanModel
from domain_evaluation.model.evaluation_criteria_plan_scope_model import EvaluationCriteriaPlanScopeModel


class EnumEvaluationAssignmentEffectedCategory(Enum):
    """
    教师、学生、家长
    """

    ESTABLISHMENT_ASSIGN = "编制分配"  # 教师、学生
    PEOPLE_RELATIONSHIP = "人员关系"  # 家长


class EvaluationAssignmentModel(VersionedModel):
    """
    评价分配
    """

    evaluation_criteria_plan_id: str
    effected_category: str
    effected_id: str
    start_at: datetime
    finish_at: Optional[datetime]


class SaveEvaluationAssignmentRelationshipModel(BasePlusModel):
    """
    保存评价标准和计划适用范围
    """
    evaluation_criteria_plan: EvaluationCriteriaPlanModel
    evaluation_criteria_plan_scope_list: List[EvaluationCriteriaPlanScopeModel]
