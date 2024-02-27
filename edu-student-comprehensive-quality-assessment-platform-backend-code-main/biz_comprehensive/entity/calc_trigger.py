from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from biz_comprehensive.entity.history.calc_trigger_history import CalcTriggerHistoryEntity


class CalcTriggerEntity(VersionedEntity):
    """
    计算触发器
    """

    __tablename__ = "st_calc_trigger"
    __table_args__ = {"comment": "计算触发器"}
    __history_entity__ = CalcTriggerHistoryEntity
    calc_rule_id = Column(String(40), comment="计算规则id", nullable=False)
    input_res_category = Column(
        String(255), comment="输入资源类别（OBSERVATION_POINT/INDICATOR）", nullable=False
    )
    input_res_id = Column(String(40), comment="输入资源id", nullable=False)
