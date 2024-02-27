"""
redis帮助类
"""


import logging
from typing import Optional

from redis.client import PubSub


def get_pubsub_message(pubsub: PubSub) -> Optional[str]:
    """
    从pubsub里获取消息体
    @param pubsub:
    @return:
    """
    message = pubsub.get_message()
    if message and "type" in message and message["type"] == "message" and "data" in message:
        logging.debug(message)
        message_content = message["data"].decode("utf-8")
        return message_content
    return None
