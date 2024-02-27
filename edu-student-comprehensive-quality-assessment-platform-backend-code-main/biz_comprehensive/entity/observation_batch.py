from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, String

from biz_comprehensive.entity.history.observation_batch_history import ObservationBatchHistoryEntity


class ObservationBatchEntity(VersionedEntity):
    """
    观测批次
    """

    __tablename__ = "st_observation_batch"
    __table_args__ = {"comment": "观测批次"}
    __history_entity__ = ObservationBatchHistoryEntity
    observation_creator_id = Column(String(40), comment="观测创建者id", nullable=False)
    plan_started_on = Column(DateTime(timezone=True), comment="计划开始时间", nullable=False)
    plan_ended_on = Column(DateTime(timezone=True), comment="计划结束时间", nullable=False)
