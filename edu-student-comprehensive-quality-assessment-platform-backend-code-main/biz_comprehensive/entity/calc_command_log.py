from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, String

from biz_comprehensive.entity.history.calc_command_log_history import CalcCommandLogHistoryEntity


class CalcCommandLogEntity(VersionedEntity):
    """
    计算命令日志
    """

    __tablename__ = "st_calc_command_log"
    __table_args__ = {"comment": "计算命令日志"}
    __history_entity__ = CalcCommandLogHistoryEntity
    calc_command_template_id = Column(String(40), comment="计算命令模板id", nullable=False)
    invoked_res_category = Column(String(255), comment="被调用资源类别（ROBOT/PEOPLE）", nullable=False)
    invoked_res_id = Column(String(40), comment="被调用资源id", nullable=False)
    invoked_on = Column(DateTime(timezone=True), comment="被调用时间", nullable=False)
