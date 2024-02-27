"""
定时任务  历史实体类
"""
from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Boolean, Column, DateTime, Index, String, text
from sqlalchemy.dialects.postgresql import JSONB


class SchedulerJobHistoryEntity(HistoryEntity):
    """
    定时任务  历史实体类
    """

    __tablename__ = "st_scheduler_job_history"
    __table_args__ = {"comment": "定时任务"}

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
    "idx_scheduler_job_history_time_range",
    SchedulerJobHistoryEntity.id,
    SchedulerJobHistoryEntity.commenced_on,
    SchedulerJobHistoryEntity.ceased_on.desc(),
    unique=True,
)

Index(
    "st_scheduler_job_history_idx_source_res",
    SchedulerJobHistoryEntity.source_res_category,
    SchedulerJobHistoryEntity.source_res_id,
)
