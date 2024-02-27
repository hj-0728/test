from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB

from infra_backbone.entity.history.distributed_task_log_history import (
    DistributedTaskLogHistoryEntity,
)


class DistributedTaskLogEntity(VersionedEntity):
    """
    Pubsub中的任务处理日志
    """

    __tablename__ = "st_distributed_task_log"
    __table_args__ = {"comment": "Pubsub中的任务处理日志"}
    __history_entity__ = DistributedTaskLogHistoryEntity

    source_res_category = Column(
        String(255), nullable=True, comment="来源资源类型（OBSERVATION_POINT_LOG/CALC_COMMAND_LOG）"
    )
    source_res_id = Column(String(40), nullable=True, comment="来源资源id")
    status = Column(String(255), nullable=False, comment="状态（READY/IN_PROCESS/SUCCEED/FAILED）")
    task_func = Column(String(255), nullable=False, comment="任务的方法名")
    task_args = Column(JSONB, nullable=True, comment="任务的方法参数")
    try_count = Column(Integer, nullable=True, comment="尝试次数")
    err_msg = Column(Text, nullable=True, comment="错误信息")


Index(
    "st_distributed_task_log_idx_source_res",
    DistributedTaskLogEntity.source_res_category,
    DistributedTaskLogEntity.source_res_id,
)
