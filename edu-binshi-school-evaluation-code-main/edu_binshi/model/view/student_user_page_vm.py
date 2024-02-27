from typing import Optional

from edu_binshi.model.view.student_page_vm import StudentPageVm
from infra_backbone.model.user_model import UserModel


class StudentUserPageVm(StudentPageVm):
    """
    学生用户分页
    """

    user: Optional[UserModel]
