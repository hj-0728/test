from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class SceneHistoryEntity(HistoryEntity):
    """
    场景历史
    """

    __tablename__ = "st_scene_history"
    __table_args__ = {"comment": "场景历史"}
    name = Column(String(255), comment="场景名称", nullable=False)
    code = Column(String(255), comment="编码", nullable=True)


Index(
    "idx_scene_history_time_range",
    SceneHistoryEntity.id,
    SceneHistoryEntity.commenced_on,
    SceneHistoryEntity.ceased_on.desc(),
    unique=True,
)
