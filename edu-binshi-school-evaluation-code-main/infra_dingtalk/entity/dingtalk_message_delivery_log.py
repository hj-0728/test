"""
企微消息递送日志
"""

from infra_basic.basic_entity import BasicEntity
from sqlalchemy import Column, Integer, String, Text


class DingtalkMessageDeliveryLogEntity(BasicEntity):
    """
    企微消息递送日志
    """

    __tablename__ = "st_dingtalk_message_delivery_log"
    __table_args__ = {"comment": "企微消息递送日志"}
    dingtalk_corp_id = Column(String(40), comment="企微组织id", nullable=False, index=True)
    message_delivery_log_id = Column(String(40), comment="消息递送日志id", nullable=False, index=True)
    error_code = Column(Integer, comment="错误码")
    error_message = Column(Text, comment="错误信息")
