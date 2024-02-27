from enum import Enum
from typing import Any, Optional

from infra_basic.basic_model import VersionedModel


class EnumDistributedTaskLogStatus(Enum):
    """
    Pubsub中的任务处理日志状态
    """

    READY = "准备中"
    IN_PROCESS = "处理中"
    SUCCEED = "成功"
    FAILED = "失败"


class EnumDistributedTaskLogSourceResCategory(Enum):
    """
    来源资源类型
    """

    OBSERVATION_POINT_LOG = "观测点日志"
    CALC_COMMAND_LOG = "计算指令"


class DistributedTaskLogModel(VersionedModel):
    """
    Pubsub中的任务处理日志
    """

    source_res_category: Optional[str]
    source_res_id: Optional[str]
    status: Optional[str]
    task_func: str
    task_args: Optional[str]
    try_count: int = 0
    err_msg: Optional[Any]
