from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from infra_backbone.entity.history.tag_info_history import TagInfoHistoryEntity


class TagInfoEntity(VersionedEntity):
    """
    标签
    """

    __tablename__ = "st_tag_info"
    __table_args__ = {"comment": "标签"}
    __history_entity__ = TagInfoHistoryEntity

    name = Column(String(255), nullable=False, comment="名称", index=True, unique=True)
