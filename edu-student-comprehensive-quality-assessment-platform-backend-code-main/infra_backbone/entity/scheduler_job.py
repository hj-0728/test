from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Boolean, Column, DateTime, Index, String, text
from sqlalchemy.dialects.postgresql import JSONB

from infra_backbone.entity.history.scheduler_job_history import SchedulerJobHistoryEntity


class SchedulerJobEntity(VersionedEntity):
    """
    定时任务
    """

    __tablename__ = "st_scheduler_job"
    __table_args__ = {"comment": "定时任务"}
    __history_entity__ = SchedulerJobHistoryEntity

    source_res_category = Column(String(255), nullable=True, comment="来源资源类型")
    source_res_id = Column(String(40), nullable=True, comment="来源资源id")
    trigger_category = Column(String(255), nullable=False, comment="触发类型")
    trigger_expression = Column(String(255), nullable=False, comment="触发表达式")
    started_on = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="开始时间",
        server_default=text("now()"),
    )
    ended_on = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="结束时间",
        server_default=text("'infinity'::timestamptz"),
    )
    is_activated = Column(Boolean, nullable=False, comment="是否激活", server_default=text("true"))
    func_name = Column(String(255), nullable=False, comment="调用的方法名")
    func_args = Column(JSONB, nullable=True, comment="方法的参数")


Index(
    "st_scheduler_job_idx_source_res",
    SchedulerJobEntity.source_res_category,
    SchedulerJobEntity.source_res_id,
)
