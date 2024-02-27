from datetime import datetime
from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel
from infra_utility.base_plus_model import BasePlusModel

from backend.model.edit.save_evaluation_criteria_plan_scope_em import (
    SaveEvaluationCriteriaPlanScopeEm,
)


class EnumEvaluationCriteriaPlanStatus(Enum):
    """
    评价标准计划状态枚举
    """

    DRAFT = "草稿"
    PUBLISHED = "已发布"
    ABOLISHED = "已废除"
    ARCHIVED = "已归档"
    IN_PROGRESS = "进行中"


class EvaluationCriteriaPlanModel(VersionedModel):
    """
    评价标准计划
    """

    evaluation_criteria_id: Optional[str]
    focus_period_id: Optional[str]
    name: Optional[str]
    executed_start_at: Optional[datetime]
    executed_finish_at: Optional[datetime]
    status: Optional[str]
    status_name: Optional[str]
    evaluation_criteria_name: Optional[str]
    report_category: Optional[str]


class SaveEvaluationCriteriaPlanModel(VersionedModel):
    """
    保存评价标准
    """

    evaluation_criteria_id: str
    focus_period_id: str
    name: str
    executed_start_at: datetime
    executed_finish_at: Optional[datetime]
    status: str

    def to_evaluation_criteria_plan_model(self) -> EvaluationCriteriaPlanModel:
        return EvaluationCriteriaPlanModel(
            id=self.id,
            version=self.version,
            evaluation_criteria_id=self.evaluation_criteria_id,
            focus_period_id=self.focus_period_id,
            name=self.name,
            executed_start_at=self.executed_start_at,
            executed_finish_at=self.executed_finish_at,
            status=self.status,
        )


class SaveEvaluationCriteriaPlanAndScopeModel(BasePlusModel):
    """
    保存评价标准和计划适用范围
    """

    evaluation_criteria_plan: Optional[SaveEvaluationCriteriaPlanModel]
    evaluation_criteria_plan_scope: Optional[SaveEvaluationCriteriaPlanScopeEm]
