from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String
from sqlalchemy.dialects.postgresql import JSONB


class CalcRuleHistoryEntity(HistoryEntity):
    """
    计算规则历史
    """

    __tablename__ = "st_calc_rule_history"
    __table_args__ = {"comment": "计算规则历史"}
    belongs_to_res_category = Column(
        String(255), comment="所属资源类别（INDICATOR/SYMBOL/MEDAL/EVALUATION_CRITERIA）", nullable=False
    )
    belongs_to_res_id = Column(String(40), comment="所属资源id", nullable=False)
    pre_func = Column(String(255), comment="前置函数", nullable=True)
    pre_func_params = Column(JSONB, comment="前置函数参数", nullable=True)
    calc_func = Column(
        String(255), comment="计算函数（可能有以下算法(ASSIGN/SUM/WEIGHTING/RANGE_ASSIGN)）", nullable=False
    )
    calc_func_params = Column(JSONB, comment="计算函数参数", nullable=True)
    post_func = Column(String(255), comment="后置函数", nullable=True)
    post_func_params = Column(JSONB, comment="后置函数参数", nullable=True)


Index(
    "idx_calc_rule_history_time_range",
    CalcRuleHistoryEntity.id,
    CalcRuleHistoryEntity.commenced_on,
    CalcRuleHistoryEntity.ceased_on.desc(),
    unique=True,
)
