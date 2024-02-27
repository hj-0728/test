"""
企业钉钉同步日志
"""


from infra_basic.basic_entity import BasicEntity
from sqlalchemy import Boolean, Column, DateTime, String, Text


class DingtalkSyncLogEntity(BasicEntity):
    """
    企业钉钉同步日志
    """

    __tablename__ = "st_dingtalk_sync_log"
    __table_args__ = {"comment": "企业钉钉同步日志"}
    dingtalk_corp_id = Column(String(40), comment="企业钉钉组织的id", nullable=False, index=True)
    category = Column(String(255), comment="同步类型(inner或者k12)", nullable=False)
    direction = Column(String(255), comment="同步方向", nullable=False)
    started_on = Column(DateTime(timezone=True), comment="开始时间", nullable=False)
    ended_on = Column(DateTime(timezone=True), comment="结束时间", nullable=True)
    is_succeed = Column(Boolean, comment="是否成功", nullable=True)
    err_message = Column(Text, comment="错误信息", nullable=True)
