from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, Integer, String

from biz_comprehensive.entity.history.observation_creator_arrange_history import (
    ObservationCreatorArrangeHistoryEntity,
)


class ObservationCreatorArrangeEntity(VersionedEntity):
    """
    观测者编排
    """

    __tablename__ = "st_observation_creator_arrange"
    __table_args__ = {"comment": "观测者编排"}
    __history_entity__ = ObservationCreatorArrangeHistoryEntity
    observation_creator_id = Column(String(40), comment="观测者id", nullable=False)
    frequency = Column(Integer, comment="频次（ONCE/SCHEDULE）", nullable=False)
    once_sent_on = Column(DateTime(timezone=True), comment="一次性的定时发送时间或者现在", nullable=True)
    schedule_weekdays = Column(Integer, comment="定时发送星期几（循环的星期周几，数组，从0-6）", nullable=True)
    schedule_sent_at = Column(DateTime(timezone=True), comment="定时发送时间（整点即可，0-23）", nullable=True)
    schedule_keep_alive_hours = Column(
        Integer, comment="定时发送保持活跃时间（循环中的活动保留几小时内填写，用整数）", nullable=True
    )
