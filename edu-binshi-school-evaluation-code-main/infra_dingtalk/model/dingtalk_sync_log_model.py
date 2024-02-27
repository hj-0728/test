"""
钉钉同步日志
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from infra_basic.basic_model import BasePlusModel


class EnumDingtalkSyncLogCategory(Enum):
    """
    同步类型
    """

    INNER = "内部通讯录同步"
    K12 = "K12（家校通讯录）同步"


class EnumDingtalkSyncLogDirection(Enum):
    """
    同步方向
    """

    REMOTE_TO_LOCAL = "远程到本地"


class DingtalkSyncLogModel(BasePlusModel):
    """
    钉钉同步日志
    """

    remark: Optional[str]
    dingtalk_corp_id: str
    category: str
    direction: str
    begin_at: datetime
    end_at: datetime
    is_succeed: bool = True
    err_message: Optional[str]
