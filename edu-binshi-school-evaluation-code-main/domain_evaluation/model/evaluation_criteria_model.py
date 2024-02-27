from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel


class EnumEvaluationCriteriaStatus(Enum):
    """
    评价标准状态枚举
    """

    DRAFT = "草稿"
    PUBLISHED = "已发布"
    ABOLISHED = "已作废"


class EnumEvaluationObjectCategory(Enum):
    """
    评价对象类型枚举
    """

    STUDENT = "学生"
    PARENTS = "家长"
    TEACHER = "老师"


class EvaluationCriteriaModel(VersionedModel):
    """
    评价标准
    """

    name: str
    status: str
    status_display: Optional[str]
    comments: Optional[str]
    evaluation_object_category: Optional[str]
    evaluation_object_category_display: Optional[str]


class SaveEvaluationCriteriaModel(VersionedModel):
    """
    保存评价标准
    """

    name: str
    status: str
    comments: Optional[str]
    evaluation_object_category: Optional[str]

    def to_evaluation_criteria_model(self) -> EvaluationCriteriaModel:
        return EvaluationCriteriaModel(
            id=self.id,
            version=self.version,
            name=self.name,
            status=self.status,
            comments=self.comments,
            evaluation_object_category=self.evaluation_object_category,
        )
