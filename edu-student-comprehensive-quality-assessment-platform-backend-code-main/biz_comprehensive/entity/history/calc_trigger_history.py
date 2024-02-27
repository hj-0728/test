from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class CalcTriggerHistoryEntity(HistoryEntity):
    """
    计算触发器历史
    """

    __tablename__ = "st_calc_trigger_history"
    __table_args__ = {"comment": "计算触发器历史"}
    calc_rule_id = Column(String(40), comment="计算规则id", nullable=False)
    input_res_category = Column(
        String(255), comment="输入资源类别（OBSERVATION_POINT/INDICATOR）", nullable=False
    )
    input_res_id = Column(String(40), comment="输入资源id", nullable=False)


Index(
    "idx_calc_trigger_history_time_range",
    CalcTriggerHistoryEntity.id,
    CalcTriggerHistoryEntity.commenced_on,
    CalcTriggerHistoryEntity.ceased_on.desc(),
    unique=True,
)
