"""
部门学生关系历史表
"""


from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class DingtalkK12DeptStudentHistoryEntity(HistoryEntity):
    """
    K12部门学生关系历史表
    """

    __tablename__ = "st_dingtalk_k12_dept_student_history"
    __table_args__ = {"comment": "K12部门学生关系历史表"}
    dingtalk_k12_student_id = Column(String(40), comment="学生id", nullable=False, index=True)
    dingtalk_k12_dept_id = Column(String(40), comment="部门id", nullable=False, index=True)


# 时间检索索引
Index(
    "idx_dingtalk_k12_dept_student_history_time_range",
    DingtalkK12DeptStudentHistoryEntity.id,
    DingtalkK12DeptStudentHistoryEntity.commenced_on,
    DingtalkK12DeptStudentHistoryEntity.ceased_on.desc(),
    unique=True,
)
