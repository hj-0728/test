"""
k12家长
"""

from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, JSON, String

from infra_dingtalk.entity.history.dingtalk_k12_parent_history import DingtalkK12ParentHistoryEntity


class DingtalkK12ParentEntity(VersionedEntity):
    """
    k12家长
    """

    __tablename__ = "st_dingtalk_k12_parent"
    __table_args__ = {"comment": "k12家长"}
    __history_entity__ = DingtalkK12ParentHistoryEntity
    dingtalk_corp_id = Column(String(40), comment="钉钉组织id", nullable=False, index=True)
    mobile = Column(String(255), comment="手机号码")
    remote_user_id = Column(String(255), comment="远程用户id", nullable=False)
    unionid = Column(String(255), comment="unionid")
    feature = Column(JSON, comment="其他属性")
