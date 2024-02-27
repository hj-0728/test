"""
钉钉应用历史
"""


from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class DingtalkAgentHistoryEntity(HistoryEntity):
    """
    钉钉应用历史
    """

    __tablename__ = "st_dingtalk_agent_history"
    __table_args__ = {"comment": "钉钉应用历史"}
    dingtalk_corp_id = Column(String(40), comment="钉钉组织id", nullable=False, index=True)
    remote_agent_id = Column(String(255), comment="远程应用id", nullable=True)
    code = Column(String(255), comment="编码", nullable=False)
    app_key = Column(String(255), comment="key", nullable=False)
    app_secret = Column(String(255), comment="密码", nullable=False)


# 时间检索索引
Index(
    "idx_dingtalk_agent_history_time_range",
    DingtalkAgentHistoryEntity.id,
    DingtalkAgentHistoryEntity.commenced_on,
    DingtalkAgentHistoryEntity.ceased_on.desc(),
    unique=True,
)
