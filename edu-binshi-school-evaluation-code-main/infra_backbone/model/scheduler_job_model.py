from datetime import datetime
from enum import Enum
from typing import Any, Optional

from infra_basic.basic_model import VersionedModel


class EnumSchedulerJobTriggerType(Enum):
    """
    定时任务触发类型
    """

    CRON = "cron间隔"
    INTERVAL = "时间间隔"


class SchedulerJobModel(VersionedModel):
    """
    定时任务
    """

    trigger_type: str
    trigger_expression: str
    start_at: Optional[datetime]
    finish_at: Optional[datetime]
    is_activated: bool = True
    func_name: str
    func_args: Optional[Any]
