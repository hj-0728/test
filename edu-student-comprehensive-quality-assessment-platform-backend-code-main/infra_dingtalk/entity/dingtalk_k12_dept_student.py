"""
k12学生部门关系
"""

from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from infra_dingtalk.entity.history.dingtalk_k12_dept_student_history import (
    DingtalkK12DeptStudentHistoryEntity,
)


class DingtalkK12DeptStudentEntity(VersionedEntity):
    """
    k12学生部门关系
    """

    __tablename__ = "st_dingtalk_k12_dept_student"
    __table_args__ = {"comment": "k12学生部门关系"}
    __history_entity__ = DingtalkK12DeptStudentHistoryEntity
    dingtalk_k12_student_id = Column(String(40), comment="学生id", nullable=False, index=True)
    dingtalk_k12_dept_id = Column(String(40), comment="部门id", nullable=False, index=True)
