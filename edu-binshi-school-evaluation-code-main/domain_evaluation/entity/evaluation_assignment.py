from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, Index, String, text

from domain_evaluation.entity.history.evaluation_assignment_history import (
    EvaluationAssignmentHistoryEntity,
)


class EvaluationAssignmentEntity(VersionedEntity):
    __tablename__ = "st_evaluation_assignment"
    __table_args__ = {"comment": "评价分配"}
    __history_entity__ = EvaluationAssignmentHistoryEntity

    evaluation_criteria_plan_id = Column(String(40), nullable=False, comment="评价标准id", index=True)
    effected_category = Column(String(255), nullable=False, comment="范围类型")
    effected_id = Column(String(40), nullable=False, comment="范围id")
    start_at = Column(DateTime(timezone=True), nullable=False, comment="开始时间")
    finish_at = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="结束时间（默认infinity，如果被删加上时间）",
        server_default=text("'infinity'::timestamptz"),
    )


Index(
    "idx_evaluation_assignment_start_finish_time_range",
    EvaluationAssignmentEntity.id,
    EvaluationAssignmentEntity.start_at,
    EvaluationAssignmentEntity.finish_at.desc(),
    unique=True,
)


Index(
    "ix_st_evaluation_assignment_effected",
    EvaluationAssignmentEntity.effected_category,
    EvaluationAssignmentEntity.effected_id,
)
