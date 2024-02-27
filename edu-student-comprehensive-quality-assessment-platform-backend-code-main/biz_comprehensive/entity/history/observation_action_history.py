from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, DateTime, Index, String


class ObservationActionHistoryEntity(HistoryEntity):
    """
    观测动作历史
    """

    __tablename__ = "st_observation_action_history"
    __table_args__ = {"comment": "观测动作历史"}
    observation_require_id = Column(String(40), comment="观测要求id", nullable=True)
    performer_res_category = Column(String(255), comment="执行者资源类别（PEOPLE）", nullable=False)
    performer_res_id = Column(String(40), comment="执行者资源id", nullable=False)
    performed_started_on = Column(DateTime(timezone=True), comment="执行开始时间", nullable=True)
    performed_ended_on = Column(DateTime(timezone=True), comment="执行结束时间", nullable=True)


Index(
    "idx_observation_action_history_time_range",
    ObservationActionHistoryEntity.id,
    ObservationActionHistoryEntity.commenced_on,
    ObservationActionHistoryEntity.ceased_on.desc(),
    unique=True,
)


Index(
    "idx_observation_action_history_performer_res",
    ObservationActionHistoryEntity.performer_res_category,
    ObservationActionHistoryEntity.performer_res_id,
)
