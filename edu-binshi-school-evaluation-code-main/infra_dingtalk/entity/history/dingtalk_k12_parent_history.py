"""
k12家长历史表
"""


from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, JSON, String


class DingtalkK12ParentHistoryEntity(HistoryEntity):
    """
    k12家长历史表
    """

    __tablename__ = "st_dingtalk_k12_parent_history"
    __table_args__ = {"comment": "k12家长历史表"}
    dingtalk_corp_id = Column(String(40), comment="钉钉组织id", nullable=False, index=True)
    mobile = Column(String(255), comment="手机号码")
    remote_user_id = Column(String(255), comment="远程用户id", nullable=False)
    unionid = Column(String(255), comment="unionid")
    feature = Column(JSON, comment="其他属性")
