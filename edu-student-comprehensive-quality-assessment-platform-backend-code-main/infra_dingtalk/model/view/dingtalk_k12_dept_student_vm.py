"""
钉钉 k12 部门、学生
"""

from infra_basic.basic_model import BasePlusModel


class DingtalkK12DeptStudentViewModel(BasePlusModel):
    """
    钉钉 k12 部门、学生
    """

    id: str
    version: int
    remote_dept_id: int
