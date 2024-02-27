from typing import Optional

from infra_basic.basic_model import BasePlusModel


class EvaluationReportAssignmentViewModel(BasePlusModel):
    evaluation_assignment_id: str
    people_name: str
    dept_name: str
    establishment_assign_id: Optional[str]
    report_file_id: Optional[str]

    grade_name: Optional[str]
    class_name: Optional[str]
