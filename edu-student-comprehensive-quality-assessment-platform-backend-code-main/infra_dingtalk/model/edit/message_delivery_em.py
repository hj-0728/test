"""
消息 参数
"""
from typing import Optional

from infra_basic.basic_model import BasePlusModel


class MessageDeliveryEm(BasePlusModel):
    message_delivery_log_id: str
    display_category: str
    user_id: str
    url: Optional[str]
    title: Optional[str]
    content: Optional[str]
