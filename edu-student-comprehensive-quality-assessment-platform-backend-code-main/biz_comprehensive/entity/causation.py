from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, String

from biz_comprehensive.entity.history.causation_history import CausationHistoryEntity


class CausationEntity(VersionedEntity):
    """
    因果关系
    """

    __tablename__ = "st_causation"
    __table_args__ = {"comment": "因果关系"}
    __history_entity__ = CausationHistoryEntity
    cause_res_category = Column(
        String(255), comment="因资源类别（OBSERVATION_POINT_LOG/CALC_COMMAND_LOG）", nullable=False
    )
    cause_res_id = Column(String(40), comment="因资源id", nullable=False)
    effect_res_category = Column(
        String(255),
        comment="果资源类别（CALC_LOG/MEDAL_ISSUE_LOG/INDICATOR_SCORE_LOG/POINTS_LOG）",
        nullable=False,
    )
    effect_res_id = Column(String(40), comment="果资源id", nullable=False)
    effected_on = Column(DateTime(timezone=True), comment="生效时间", nullable=False)
