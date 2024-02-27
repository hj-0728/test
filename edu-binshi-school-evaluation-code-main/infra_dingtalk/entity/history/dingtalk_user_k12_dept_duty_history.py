"""
用户在k12部门中的职责历史表
"""


from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, String


class DingtalkUserK12DeptDutyHistoryEntity(HistoryEntity):
    """
    用户在k12部门中的职责历史表
    """

    __tablename__ = "st_dingtalk_user_k12_dept_duty_history"
    __table_args__ = {"comment": "用户在k12部门中的职责历史表"}
    dingtalk_user_id = Column(String(40), comment="用户id", nullable=False, index=True)
    dingtalk_k12_dept_id = Column(String(40), comment="k12部门id", nullable=False, index=True)
    duty = Column(String(255), comment="职责", nullable=False)
    subject = Column(String(255), comment="科目")
