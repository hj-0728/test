from typing import Optional

from edu_binshi.model.report_record_model import ReportRecordModel


class ReportRecordViewModel(ReportRecordModel):
    """
    报告记录 view model
    """

    current_role_code: Optional[str]
    current_people_id: Optional[str]
