from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class ReportRecordEvalAssignMapHistoryEntity(HistoryEntity):
    """
    报告记录评价分配map（历史实体类）
    """

    __tablename__ = "st_report_record_eval_assign_map_history"
    __table_args__ = {"comment": "报告记录评价分配map（历史）"}
    report_record_id = Column(String(40), comment="报告记录id", nullable=False)
    evaluation_assignment_id = Column(String(40), comment="评价分配id", nullable=False)


Index(
    "idx_report_record_eval_assign_map_history_time_range",
    ReportRecordEvalAssignMapHistoryEntity.id,
    ReportRecordEvalAssignMapHistoryEntity.begin_at,
    ReportRecordEvalAssignMapHistoryEntity.end_at.desc(),
    unique=True,
)
