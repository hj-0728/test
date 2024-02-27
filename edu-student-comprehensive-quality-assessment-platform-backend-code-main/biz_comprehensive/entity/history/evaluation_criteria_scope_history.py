from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class EvaluationCriteriaScopeHistoryEntity(HistoryEntity):
    """
    评价标准范围历史
    """

    __tablename__ = "st_evaluation_criteria_scope_history"
    __table_args__ = {"comment": "评价标准范围历史"}
    evaluation_criteria_id = Column(String(40), comment="评价标准id", nullable=False)
    effected_res_category = Column(
        String(255), comment="生效资源类别（DIMENSION_DEPT_TREE）", nullable=False
    )
    effected_res_id = Column(String(40), comment="生效资源id", nullable=False)


Index(
    "idx_evaluation_criteria_scope_history_time_range",
    EvaluationCriteriaScopeHistoryEntity.id,
    EvaluationCriteriaScopeHistoryEntity.commenced_on,
    EvaluationCriteriaScopeHistoryEntity.ceased_on.desc(),
    unique=True,
)
