from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, Index, String

from biz_comprehensive.entity.history.observation_action_history import (
    ObservationActionHistoryEntity,
)


class ObservationActionEntity(VersionedEntity):
    """
    观测动作
    """

    __tablename__ = "st_observation_action"
    __table_args__ = {"comment": "观测动作"}
    __history_entity__ = ObservationActionHistoryEntity
    observation_require_id = Column(String(40), comment="观测要求id", nullable=True, index=True)
    performer_res_category = Column(String(255), comment="执行者资源类别（PEOPLE）", nullable=False)
    performer_res_id = Column(String(40), comment="执行者资源id", nullable=False)
    performed_started_on = Column(DateTime(timezone=True), comment="执行开始时间", nullable=True)
    performed_ended_on = Column(DateTime(timezone=True), comment="执行结束时间", nullable=True)


Index(
    "idx_observation_action_performer_res",
    ObservationActionEntity.performer_res_category,
    ObservationActionEntity.performer_res_id,
)
