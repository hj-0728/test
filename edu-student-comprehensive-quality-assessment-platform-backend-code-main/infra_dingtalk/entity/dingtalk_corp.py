"""
钉钉组织
"""

from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from infra_dingtalk.entity.history.dingtalk_corp_history import DingtalkCorpHistoryEntity


class DingtalkCorpEntity(VersionedEntity):
    """
    钉钉组织
    """

    __tablename__ = "st_dingtalk_corp"
    __table_args__ = {"comment": "钉钉组织"}
    __history_entity__ = DingtalkCorpHistoryEntity
    remote_corp_id = Column(String(255), comment="远程组织id", nullable=False, unique=True)
    name = Column(String(255), comment="名称", nullable=False)
