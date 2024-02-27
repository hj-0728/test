from datetime import datetime
from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel


class EnumContextSyncLogCategory(Enum):
    """
    同步类型
    """

    DEPT = "部门同步"
    INNER_USER = "用户同步"
    PARENT_AND_STUDENT = "家长学生同步"


class EnumContextSyncDirection(Enum):
    """
    同步方向
    """

    DINGTALK_TO_CORE = "钉钉到核心"


class ContextSyncLogModel(VersionedModel):
    """
    上下文同步日志
    """

    category: str
    direction: str
    started_on: datetime
    ended_on: Optional[datetime]
    is_succeed: bool = True
    err_message: Optional[str]
