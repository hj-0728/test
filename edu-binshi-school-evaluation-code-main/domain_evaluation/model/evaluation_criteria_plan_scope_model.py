from datetime import datetime
from enum import Enum
from typing import List, Optional

from infra_basic.basic_model import VersionedModel
from infra_utility.base_plus_model import BasePlusModel


class EnumGroupCategory(Enum):
    """
    小组、部门、组织
    """

    GROUP = "小组"
    DEPT = "部门"
    PERSONAL = "个人"


class EvaluationCriteriaPlanScopeModel(VersionedModel):
    """
    评价标准适用的集合
    """

    evaluation_criteria_plan_id: str
    scope_category: str
    scope_id: str
    start_at: datetime
    finish_at: Optional[datetime]


class SaveEvaluationCriteriaPlanScopeModel(VersionedModel):
    """
    评价标准适用的集合
    """

    evaluation_criteria_plan_id: str
    scope_category: Optional[str]
    scope_id: Optional[str]
    evaluation_object_category: Optional[str]

    def to_evaluation_criteria_plan_scope_model(self) -> EvaluationCriteriaPlanScopeModel:
        return EvaluationCriteriaPlanScopeModel(
            id=self.id,
            version=self.version,
            evaluation_criteria_plan_id=self.evaluation_criteria_plan_id,
            scope_category=self.scope_category,
            scope_id=self.scope_id,
        )


class ScopeInfo(BasePlusModel):
    """
    范围信息
    """

    id: str
    name: str
    is_deleted: Optional[bool]


class EvaluationCriteriaPlanScopeCategoryModal(BasePlusModel):
    """
    评价使用集合类别
    """

    scope_category: Optional[str]
    scope_info: Optional[List[ScopeInfo]]
