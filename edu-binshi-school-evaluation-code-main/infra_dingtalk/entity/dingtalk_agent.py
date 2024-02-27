"""
钉钉应用
"""

from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from infra_dingtalk.entity.history.dingtalk_agent_history import DingtalkAgentHistoryEntity


class DingtalkAgentEntity(VersionedEntity):
    """
    钉钉应用
    """

    __tablename__ = "st_dingtalk_agent"
    __table_args__ = {"comment": "钉钉应用"}
    __history_entity__ = DingtalkAgentHistoryEntity
    dingtalk_corp_id = Column(String(40), comment="钉钉组织id", nullable=False, index=True)
    remote_agent_id = Column(String(255), comment="远程应用id", nullable=True)
    code = Column(String(255), comment="编码", nullable=False)
    app_key = Column(String(255), comment="key", nullable=False)
    app_secret = Column(String(255), comment="密码", nullable=False)
