from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class CalcCommandLogScopeHistoryEntity(HistoryEntity):
    """
    计算命令日志范围历史
    """

    __tablename__ = "st_calc_command_log_scope_history"
    __table_args__ = {"comment": "计算命令日志范围历史"}
    calc_command_log_id = Column(String(40), comment="计算命令日志id", nullable=False)
    scope_res_category = Column(String(255), comment="范围资源类别（DIMENSION_DEPT_TREE）", nullable=False)
    scope_res_id = Column(String(40), comment="范围资源id", nullable=False)


Index(
    "idx_calc_command_log_scope_history_time_range",
    CalcCommandLogScopeHistoryEntity.id,
    CalcCommandLogScopeHistoryEntity.commenced_on,
    CalcCommandLogScopeHistoryEntity.ceased_on.desc(),
    unique=True,
)
