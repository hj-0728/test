from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, DateTime, Index, String


class ObservationBatchHistoryEntity(HistoryEntity):
    """
    观测批次历史
    """

    __tablename__ = "st_observation_batch_history"
    __table_args__ = {"comment": "观测批次历史"}
    observation_creator_id = Column(String(40), comment="观测创建者id", nullable=False)
    plan_started_on = Column(DateTime(timezone=True), comment="计划开始时间", nullable=False)
    plan_ended_on = Column(DateTime(timezone=True), comment="计划结束时间", nullable=False)


Index(
    "idx_observation_batch_history_time_range",
    ObservationBatchHistoryEntity.id,
    ObservationBatchHistoryEntity.commenced_on,
    ObservationBatchHistoryEntity.ceased_on.desc(),
    unique=True,
)
