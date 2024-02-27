from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from biz_comprehensive.entity.history.scene_history import SceneHistoryEntity


class SceneEntity(VersionedEntity):
    """
    场景
    """

    __tablename__ = "st_scene"
    __table_args__ = {"comment": "场景 "}
    __history_entity__ = SceneHistoryEntity
    name = Column(String(255), comment="场景名称", nullable=False)
    code = Column(String(255), comment="编码", nullable=True)
