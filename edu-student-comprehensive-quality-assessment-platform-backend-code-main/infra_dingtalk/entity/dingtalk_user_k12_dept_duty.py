"""
用户在k12部门中的职责
"""

from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from infra_dingtalk.entity.history.dingtalk_user_k12_dept_duty_history import (
    DingtalkUserK12DeptDutyHistoryEntity,
)


class DingtalkUserK12DeptDutyEntity(VersionedEntity):
    """
    用户在k12部门中的职责
    """

    __tablename__ = "st_dingtalk_user_k12_dept_duty"
    __table_args__ = {"comment": "用户在k12部门中的职责"}
    __history_entity__ = DingtalkUserK12DeptDutyHistoryEntity
    dingtalk_user_id = Column(String(40), comment="用户id", nullable=False, index=True)
    dingtalk_k12_dept_id = Column(String(40), comment="k12部门id", nullable=False, index=True)
    duty = Column(String(255), comment="职责", nullable=False)
    subject = Column(String(255), comment="科目")
