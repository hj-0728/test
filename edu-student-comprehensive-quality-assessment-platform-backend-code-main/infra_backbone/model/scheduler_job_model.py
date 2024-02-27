from datetime import datetime
from enum import Enum
from typing import Any, Optional

from infra_basic.basic_model import VersionedModel


class EnumSchedulerJobTriggerCategory(Enum):
    """
    定时任务触发类型
    """

    CRON = "cron间隔"
    INTERVAL = "时间间隔"


class SchedulerJobModel(VersionedModel):
    """
    定时任务
    """

    source_res_category: Optional[str]
    source_res_id: Optional[str]
    trigger_category: str
    trigger_expression: str
    started_on: Optional[datetime]
    ended_on: Optional[datetime]
    is_activated: bool = True
    func_name: str
    func_args: Optional[Any]
