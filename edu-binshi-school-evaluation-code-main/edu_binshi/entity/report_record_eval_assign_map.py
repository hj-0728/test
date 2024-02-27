from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from edu_binshi.entity.history.report_record_eval_assign_map_history import \
    ReportRecordEvalAssignMapHistoryEntity


class ReportRecordEvalAssignMapEntity(VersionedEntity):
    """
    报告记录评价分配map
    """

    __tablename__ = "st_report_record_eval_assign_map"
    __table_args__ = {"comment": "报告记录评价分配map"}
    __history_entity__ = ReportRecordEvalAssignMapHistoryEntity
    report_record_id = Column(String(40), comment="报告记录id", nullable=False)
    evaluation_assignment_id = Column(String(40), comment="评价分配id", nullable=False)
