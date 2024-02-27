from infra_basic.basic_entity import BasicEntity
from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import JSONB


class AccessLogEntity(BasicEntity):
    """
    访问日志
    """

    __tablename__ = "st_access_log"
    __table_args__ = {"comment": "访问日志"}
    access_at = Column(DateTime(timezone=True), comment="访问时间", nullable=False)
    visitor_category = Column(String(255), comment="访问者类型")
    visitor_id = Column(String(255), comment="访问者id")
    ip = Column(String(255), comment="IP信息")
    destination = Column(Text, comment="访问地址", nullable=False)
    args = Column(JSONB, comment="访问所带参数")
    user_agent = Column(Text, comment="用户代理")
    footprint = Column(JSONB, comment="足迹")
