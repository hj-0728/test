from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, Index, String

from biz_comprehensive.entity.history.observation_action_produce_history import (
    ObservationActionProduceHistoryEntity,
)


class ObservationActionProduceEntity(VersionedEntity):
    """
    观测动作产出
    """

    __tablename__ = "st_observation_action_produce"
    __table_args__ = {"comment": "观测动作产出"}
    __history_entity__ = ObservationActionProduceHistoryEntity
    observation_action_id = Column(String(40), comment="观测动作id", nullable=False, index=True)
    produce_res_category = Column(
        String(255),
        comment="产出资源类别（OBSERVATION_POINT_LOG/CREATIONS/MOMENTS/TODO_RESULT/ASSESSMENT_RESULT）",
        nullable=False,
    )
    produce_res_id = Column(String(40), comment="产出资源id", nullable=False)


Index(
    "idx_observation_action_produce_produce_res",
    ObservationActionProduceEntity.produce_res_category,
    ObservationActionProduceEntity.produce_res_id,
)
