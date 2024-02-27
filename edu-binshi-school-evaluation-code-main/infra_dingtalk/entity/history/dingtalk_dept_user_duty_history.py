"""
部门用户职责历史表
"""


from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Boolean, Column, Integer, String


class DingtalkDeptUserDutyHistoryEntity(HistoryEntity):
    """
    部门用户职责历史表
    """

    __tablename__ = "st_dingtalk_dept_user_duty_history"
    __table_args__ = {"comment": "部门用户职责历史表"}
    dingtalk_user_id = Column(String(40), comment="用户id", nullable=False, index=True)
    dingtalk_dept_id = Column(String(40), comment="部门id", nullable=False, index=True)
    duty = Column(String(255), comment="职责", nullable=False)
    seq = Column(Integer, comment="部门排序", nullable=False)
