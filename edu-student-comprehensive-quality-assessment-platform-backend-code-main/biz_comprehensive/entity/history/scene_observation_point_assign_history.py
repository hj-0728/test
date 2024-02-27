from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class SceneObservationPointAssignHistoryEntity(HistoryEntity):
    """
    场景观测点分配历史
    """

    __tablename__ = "st_scene_observation_point_assign_history"
    __table_args__ = {"comment": "场景观测点分配历史"}
    scene_id = Column(String(40), comment="场景id", nullable=False, index=True)
    observation_point_id = Column(String(40), comment="观测点id", nullable=False, index=True)


Index(
    "idx_scene_observation_point_assign_history_time_range",
    SceneObservationPointAssignHistoryEntity.id,
    SceneObservationPointAssignHistoryEntity.commenced_on,
    SceneObservationPointAssignHistoryEntity.ceased_on.desc(),
    unique=True,
)
