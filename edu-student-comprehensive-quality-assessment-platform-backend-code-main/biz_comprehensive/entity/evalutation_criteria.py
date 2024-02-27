from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String, Text

from biz_comprehensive.entity.history.evaluation_criteria_history import (
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
    code = Column(String(255), comment="编码", nullable=True)
    status = Column(String(255), comment="状态（PUBLISHED/ARCHIVE/ABOLISHED）", nullable=False)
    comment = Column(Text, comment="描述", nullable=True)
    evaluation_object_category = Column(String(255), comment="评价对象类型（学生、家长、老师等）", nullable=False)
    period_id = Column(String(40), comment="周期id（每个学期都clone一下重新开始）", nullable=False)
