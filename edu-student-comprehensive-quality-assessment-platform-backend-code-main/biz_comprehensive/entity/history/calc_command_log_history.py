from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, DateTime, Index, String


class CalcCommandLogHistoryEntity(HistoryEntity):
    """
    计算命令日志历史
    """

    __tablename__ = "st_calc_command_log_history"
    __table_args__ = {"comment": "计算命令日志历史"}
    calc_command_template_id = Column(String(40), comment="计算命令模板id", nullable=False)
    invoked_res_category = Column(String(255), comment="被调用资源类别（ROBOT/PEOPLE）", nullable=False)
    invoked_res_id = Column(String(40), comment="被调用资源id", nullable=False)
    invoked_on = Column(DateTime(timezone=True), comment="被调用时间", nullable=False)


Index(
    "idx_calc_command_log_history_time_range",
    CalcCommandLogHistoryEntity.id,
    CalcCommandLogHistoryEntity.commenced_on,
    CalcCommandLogHistoryEntity.ceased_on.desc(),
    unique=True,
)
