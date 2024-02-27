from infra_basic.basic_entity import BasicEntity
from sqlalchemy import Boolean, Column, DateTime, String, Text


class SchedulerJobLogEntity(BasicEntity):
    """
    定时任务日志
    """

    __tablename__ = "st_scheduler_job_log"
    __table_args__ = {"comment": "定时任务日志"}

    scheduler_job_id = Column(String(40), nullable=False, comment="定时任务id", index=True)
    execute_start_at = Column(DateTime(timezone=True), nullable=False, comment="开始时间")
    execute_finish_at = Column(DateTime(timezone=True), nullable=False, comment="结束时间")
    is_succeed = Column(Boolean, nullable=False, comment="是否成功")
    execute_result = Column(Text, nullable=True, comment="执行结果")
