from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import JSONB

from biz_comprehensive.entity.history.calc_log_history import CalcLogHistoryEntity


class CalcLogEntity(VersionedEntity):
    """
    计算日志
    """

    __tablename__ = "st_calc_log"
    __table_args__ = {"comment": "计算日志"}
    __history_entity__ = CalcLogHistoryEntity
    calc_rule_id = Column(String(40), comment="计算规则id", nullable=False)
    calc_on = Column(DateTime(timezone=True), comment="计算时间", nullable=False)
    pre_func = Column(String(255), comment="前置函数", nullable=True)
    pre_func_args = Column(JSONB, comment="前置函数参数", nullable=True)
    calc_func = Column(
        String(255), comment="计算函数（可能有以下算法(ASSIGN/SUM/WEIGHTING/RANGE_ASSIGN)）", nullable=False
    )
    calc_func_args = Column(JSONB, comment="计算函数参数", nullable=True)
    post_func = Column(String(255), comment="后置函数，负责完成后的工作", nullable=True)
    post_func_args = Column(JSONB, comment="后置函数参数", nullable=True)
    calc_result = Column(JSONB, comment="计算结果", nullable=False)
