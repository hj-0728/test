"""
钉钉事件监听数据
"""
from typing import Optional

from infra_basic.basic_model import VersionedModel


class DingTalkEventListenerDataModel(VersionedModel):
    """
    钉钉事件监听数据
    """

    code: str
    event_listener_data: str
    md5: str
    nonce: str
    signature: str
    timestamp: int
    plain_text: Optional[str]
