from typing import Optional

from infra_utility.base_plus_model import BasePlusModel


class StudentPageVm(BasePlusModel):
    """
    学生分页
    """

    student_name: str
    people_id: str
    establishment_assign_id: Optional[str]
    school_class: str
    grade: str
