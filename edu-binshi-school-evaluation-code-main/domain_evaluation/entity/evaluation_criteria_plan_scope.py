from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, String, text

from domain_evaluation.entity.history.evaluation_criteria_plan_scope_history import (
    EvaluationCriteriaPlanScopeHistoryEntity,
)


class EvaluationCriteriaPlanScopeEntity(VersionedEntity):
    __tablename__ = "st_evaluation_criteria_plan_scope"
    __table_args__ = {"comment": "评价计划适用的集合"}
    __history_entity__ = EvaluationCriteriaPlanScopeHistoryEntity

    evaluation_criteria_plan_id = Column(String(40), nullable=False, comment="评价标准id", index=True)
    scope_category = Column(String(255), nullable=False, comment="范围类型（小组、部门、个人）")
    scope_id = Column(String(40), nullable=False, comment="范围id")
    start_at = Column(DateTime(timezone=True), nullable=False, comment="开始时间")
    finish_at = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="结束时间（默认infinity，如果被删加上时间）",
        server_default=text("'infinity'::timestamptz"),
    )
