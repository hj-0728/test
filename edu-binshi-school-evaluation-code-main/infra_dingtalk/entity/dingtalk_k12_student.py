"""
k12学生
"""

from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, JSON, String

from infra_dingtalk.entity.history.dingtalk_k12_student_history import (
    DingtalkK12StudentHistoryEntity,
)


class DingtalkK12StudentEntity(VersionedEntity):
    """
    k12学生
    """

    __tablename__ = "st_dingtalk_k12_student"
    __table_args__ = {"comment": "k12学生"}
    __history_entity__ = DingtalkK12StudentHistoryEntity
    dingtalk_corp_id = Column(String(40), comment="钉钉组织id", nullable=False, index=True)
    remote_user_id = Column(String(255), comment="远程用户id", nullable=False)
    unionid = Column(String(255), comment="unionid")
    name = Column(String(255), comment="用户名", nullable=False)
    feature = Column(JSON, comment="其他属性")
