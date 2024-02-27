from infra_basic.basic_model import VersionedModel


class ReportRecordEvalAssignMapModel(VersionedModel):
    """
    报告记录评价分配map model
    """

    report_record_id: str
    evaluation_assignment_id: str
