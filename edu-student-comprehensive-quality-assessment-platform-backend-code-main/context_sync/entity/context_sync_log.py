"""
上下文同步日志
"""

from infra_basic.basic_entity import BasicEntity
from sqlalchemy import Boolean, Column, DateTime, String, Text


class ContextSyncLogEntity(BasicEntity):
    """
    上下文同步日志
    """

    __tablename__ = "st_context_sync_log"
    __table_args__ = {"comment": "上下文同步日志"}
    category = Column(String(255), comment="同步类型(dept或是user)", nullable=False)
    direction = Column(String(255), comment="同步方向", nullable=False)
    started_on = Column(DateTime(timezone=True), comment="开始时间", nullable=False)
    ended_on = Column(DateTime(timezone=True), comment="结束时间", nullable=True)
    is_succeed = Column(Boolean, comment="是否成功", nullable=True)
    err_message = Column(Text, comment="错误信息", nullable=True)
