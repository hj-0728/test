from typing import Optional

from infra_basic.basic_model import BasePlusModel


class StudentInfoViewModel(BasePlusModel):
    """
    学生信息
    """

    id: str
    establishment_assign_id: str
    name: str
    dept_name: Optional[str]
    avatar: str
