"""
部门用户职责
"""

from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Boolean, Column, Integer, String

from infra_dingtalk.entity.history.dingtalk_dept_user_duty_history import (
    DingtalkDeptUserDutyHistoryEntity,
)


class DingtalkDeptUserDutyEntity(VersionedEntity):
    """
    部门用户职责
    """

    __tablename__ = "st_dingtalk_dept_user_duty"
    __table_args__ = {"comment": "部门用户职责"}
    __history_entity__ = DingtalkDeptUserDutyHistoryEntity
    dingtalk_user_id = Column(String(40), comment="用户id", nullable=False, index=True)
    dingtalk_dept_id = Column(String(40), comment="部门id", nullable=False, index=True)
    duty = Column(String(255), comment="职责", nullable=False)
    seq = Column(Integer, comment="部门排序", nullable=False)
