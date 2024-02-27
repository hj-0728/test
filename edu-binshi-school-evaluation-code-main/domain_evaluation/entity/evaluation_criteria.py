from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, Numeric, String, Text, text

from domain_evaluation.entity.history.evaluation_criteria_history import (
    EvaluationCriteriaHistoryEntity,
)


class EvaluationCriteriaEntity(VersionedEntity):
    """
    评价标准
    """

    __tablename__ = "st_evaluation_criteria"
    __table_args__ = {"comment": "评价标准"}
    __history_entity__ = EvaluationCriteriaHistoryEntity
    name = Column(String(255), comment="名称", nullable=False)
    status = Column(String(255), comment="状态", nullable=True)
    comments = Column(Text, comment="描述", nullable=True)
    evaluation_object_category = Column(String(255), comment="评价对象类型（学生、家长、老师等）", nullable=False)
