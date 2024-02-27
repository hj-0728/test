from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from biz_comprehensive.entity.history.calc_command_log_scope_history import (
    CalcCommandLogScopeHistoryEntity,
)


class CalcCommandLogScopeEntity(VersionedEntity):
    """
    计算命令日志范围
    """

    __tablename__ = "st_calc_command_log_scope"
    __table_args__ = {"comment": "计算命令日志范围"}
    __history_entity__ = CalcCommandLogScopeHistoryEntity
    calc_command_log_id = Column(String(40), comment="计算命令日志id", nullable=False)
    scope_res_category = Column(String(255), comment="范围资源类别（DIMENSION_DEPT_TREE）", nullable=False)
    scope_res_id = Column(String(40), comment="范围资源id", nullable=False)
