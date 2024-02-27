from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, DateTime, Index, String


class EvaluationCriteriaPlanHistoryEntity(HistoryEntity):
    __tablename__ = "st_evaluation_criteria_plan_history"
    __table_args__ = {"comment": "计划（历史）"}

    evaluation_criteria_id = Column(String(40), nullable=False, comment="评价标准id", index=True)
    focus_period_id = Column(String(40), nullable=False, comment="关联周期id")
    name = Column(String(255), nullable=False, comment="名称")
    executed_start_at = Column(DateTime(timezone=True), nullable=False, comment="开始时间")
    executed_finish_at = Column(DateTime(timezone=True), nullable=False, comment="结束时间")
    status = Column(String(255), nullable=False, comment="状态")


Index(
    "idx_evaluation_criteria_plan_history_time_range",
    EvaluationCriteriaPlanHistoryEntity.id,
    EvaluationCriteriaPlanHistoryEntity.begin_at,
    EvaluationCriteriaPlanHistoryEntity.end_at.desc(),
    unique=True,
)
