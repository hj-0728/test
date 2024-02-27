from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from biz_comprehensive.entity.history.evaluation_criteria_scope_history import (
    EvaluationCriteriaScopeHistoryEntity,
)


class EvaluationCriteriaScopeEntity(VersionedEntity):
    """
    评价标准范围
    """

    __tablename__ = "st_evaluation_criteria_scope"
    __table_args__ = {"comment": "评价标准范围"}
    __history_entity__ = EvaluationCriteriaScopeHistoryEntity
    evaluation_criteria_id = Column(String(40), comment="评价标准id", nullable=False)
    effected_res_category = Column(
        String(255), comment="生效资源类别（DIMENSION_DEPT_TREE）", nullable=False
    )
    effected_res_id = Column(String(40), comment="生效资源id", nullable=False)
