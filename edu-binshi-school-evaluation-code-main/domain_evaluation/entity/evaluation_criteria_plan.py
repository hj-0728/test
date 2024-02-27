from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, String

from domain_evaluation.entity.history.evaluation_criteria_plan_history import (
    EvaluationCriteriaPlanHistoryEntity,
)


class EvaluationCriteriaPlanEntity(VersionedEntity):
    __tablename__ = "st_evaluation_criteria_plan"
    __table_args__ = {"comment": "计划"}
    __history_entity__ = EvaluationCriteriaPlanHistoryEntity

    evaluation_criteria_id = Column(String(40), nullable=False, comment="评价标准id", index=True)
    focus_period_id = Column(String(40), nullable=False, comment="关联周期id", index=True)
    name = Column(String(255), nullable=False, comment="名称")
    executed_start_at = Column(DateTime(timezone=True), nullable=False, comment="开始时间")
    executed_finish_at = Column(DateTime(timezone=True), nullable=False, comment="结束时间")
    status = Column(String(255), nullable=False, comment="状态")
