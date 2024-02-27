from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, Numeric, String


class CalcRulePreDependsHistoryEntity(HistoryEntity):
    """
    计算规则前置依赖历史
    """

    __tablename__ = "st_calc_rule_pre_depends_history"
    __table_args__ = {"comment": "计算规则前置依赖历史"}
    calc_rule_id = Column(String(40), comment="计算规则id", nullable=False)
    depend_res_category = Column(
        String(255), comment="依赖资源类别（OBSERVATION_POINT/INDICATOR）", nullable=False
    )
    depend_res_id = Column(String(40), comment="依赖资源id", nullable=False)
    weight = Column(Numeric, comment="权重（根据category去调用对应的填写者计算的类）", nullable=False)


Index(
    "idx_calc_rule_pre_depends_history_time_range",
    CalcRulePreDependsHistoryEntity.id,
    CalcRulePreDependsHistoryEntity.commenced_on,
    CalcRulePreDependsHistoryEntity.ceased_on.desc(),
    unique=True,
)
