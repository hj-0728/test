from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, Index, String, Text

from biz_comprehensive.entity.history.observation_point_log_history import (
    ObservationPointLogHistoryEntity,
)


class ObservationPointLogEntity(VersionedEntity):
    """
    观测点日志
    """

    __tablename__ = "st_observation_point_log"
    __table_args__ = {"comment": "观测点日志"}
    __history_entity__ = ObservationPointLogHistoryEntity
    observation_point_id = Column(String(40), comment="观测点id", nullable=False, index=True)
    observee_res_category = Column(String(255), comment="被观察者类别，编制分配的id", nullable=False)
    observee_res_id = Column(String(40), comment="被观察者id", nullable=False)
    started_on = Column(
        DateTime(timezone=True),
        comment="被观察现象开始时间",
        nullable=True,
    )
    ended_on = Column(
        DateTime(timezone=True),
        comment="被观察现象结束时间",
        nullable=True,
    )
    comment = Column(Text, comment="备注", nullable=True)


Index(
    "idx_observation_point_log_observee_res",
    ObservationPointLogEntity.observee_res_category,
    ObservationPointLogEntity.observee_res_id,
)
