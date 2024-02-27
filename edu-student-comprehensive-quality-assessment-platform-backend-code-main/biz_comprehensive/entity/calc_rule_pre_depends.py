from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, Numeric, String

from biz_comprehensive.entity.history.calc_rule_pre_depends_history import (
    CalcRulePreDependsHistoryEntity,
)


class CalcRulePreDependsEntity(VersionedEntity):
    """
    计算规则前置依赖
    """

    __tablename__ = "st_calc_rule_pre_depends"
    __table_args__ = {"comment": "计算规则前置依赖"}
    __history_entity__ = CalcRulePreDependsHistoryEntity
    calc_rule_id = Column(String(40), comment="计算规则id", nullable=False)
    depend_res_category = Column(
        String(255), comment="依赖资源类别（OBSERVATION_POINT/INDICATOR）", nullable=False
    )
    depend_res_id = Column(String(40), comment="依赖资源id", nullable=False)
    weight = Column(Numeric, comment="权重（根据category去调用对应的填写者计算的类）", nullable=False)
