from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, DateTime, Index, String


class CausationHistoryEntity(HistoryEntity):
    """
    因果关系历史
    """

    __tablename__ = "st_causation_history"
    __table_args__ = {"comment": "因果关系历史"}
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


Index(
    "idx_causation_history_time_range",
    CausationHistoryEntity.id,
    CausationHistoryEntity.commenced_on,
    CausationHistoryEntity.ceased_on.desc(),
    unique=True,
)
