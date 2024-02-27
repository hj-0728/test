"""
钉钉 k12 部门、学生
"""

from infra_basic.basic_model import VersionedModel


class DingtalkK12DeptStudentModel(VersionedModel):
    """
    钉钉 k12 部门、学生
    """

    dingtalk_k12_student_id: str
    dingtalk_k12_dept_id: str
