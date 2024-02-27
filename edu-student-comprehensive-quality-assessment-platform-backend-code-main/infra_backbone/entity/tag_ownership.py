from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Boolean, Column, Index, String, text

from infra_backbone.entity.history.tag_ownership_history import TagOwnershipHistoryEntity


class TagOwnershipEntity(VersionedEntity):
    """
    标签所属
    """

    __tablename__ = "st_tag_ownership"
    __table_args__ = {"comment": "标签所属"}
    __history_entity__ = TagOwnershipHistoryEntity

    tag_id = Column(String(40), nullable=False, comment="标签id", index=True)
    code = Column(String(255), nullable=True, comment="编码", index=True)
    owner_category = Column(String(255), nullable=False, comment="所属类型")
    owner_id = Column(String(40), nullable=False, comment="所属id")
    is_editable = Column(Boolean, nullable=False, comment="是否可编辑", server_default=text("true"))
    is_activated = Column(Boolean, nullable=False, comment="是否激活", server_default=text("true"))


Index(
    "idx_tag_ownership_resource_info",
    TagOwnershipEntity.owner_category,
    TagOwnershipEntity.owner_id,
)
