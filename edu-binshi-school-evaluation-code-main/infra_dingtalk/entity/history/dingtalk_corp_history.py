"""
钉钉组织历史表
"""


from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, String


class DingtalkCorpHistoryEntity(HistoryEntity):
    """
    钉钉组织历史表
    """

    __tablename__ = "st_dingtalk_corp_history"
    __table_args__ = {"comment": "钉钉组织历史表"}
    remote_corp_id = Column(String(255), comment="远程组织id", nullable=False)
    name = Column(String(255), comment="名称", nullable=False)
