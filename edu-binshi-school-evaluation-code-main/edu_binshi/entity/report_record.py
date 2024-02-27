from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import JSONB

from edu_binshi.entity.history.report_record_history import ReportRecordHistoryEntity


class ReportRecordEntity(VersionedEntity):
    """
    报告记录
    """

    __tablename__ = "st_report_record"
    __table_args__ = {"comment": "报告记录"}
    __history_entity__ = ReportRecordHistoryEntity
    created_at = Column(DateTime(timezone=True), comment="生成时间", nullable=False)
    user_role_id = Column(String(40), comment="操作下载用户角色id", nullable=False)
    evaluation_criteria_plan_id = Column(String(40), comment="计划id", nullable=False)
    target_category = Column(String(255), comment="目标类型（比如学生）", nullable=False)
    target_id = Column(String(40), comment="目标id（比如学生）", nullable=False)
    args = Column(JSONB, comment="参数", nullable=True)
    error = Column(Text, comment="错误信息", nullable=True)
    status = Column(String(255), comment="状态", nullable=False)
