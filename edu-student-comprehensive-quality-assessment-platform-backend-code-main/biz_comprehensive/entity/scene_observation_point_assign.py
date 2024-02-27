from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from biz_comprehensive.entity.history.scene_observation_point_assign_history import (
    SceneObservationPointAssignHistoryEntity,
)


class SceneObservationPointAssignEntity(VersionedEntity):
    """
    场景观测点分配
    """

    __tablename__ = "st_scene_observation_point_assign"
    __table_args__ = {"comment": "场景观测点分配 "}
    __history_entity__ = SceneObservationPointAssignHistoryEntity
    scene_id = Column(String(40), comment="场景id", nullable=False, index=True)
    observation_point_id = Column(String(40), comment="观测点id", nullable=False, index=True)
