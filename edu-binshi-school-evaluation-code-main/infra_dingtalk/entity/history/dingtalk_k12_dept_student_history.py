"""
部门学生关系历史表
"""


from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, String


class DingtalkK12DeptStudentHistoryEntity(HistoryEntity):
    """
    K12部门学生关系历史表
    """

    __tablename__ = "st_dingtalk_k12_dept_student_history"
    __table_args__ = {"comment": "K12部门学生关系历史表"}
    dingtalk_k12_student_id = Column(String(40), comment="学生id", nullable=False, index=True)
    dingtalk_k12_dept_id = Column(String(40), comment="部门id", nullable=False, index=True)
