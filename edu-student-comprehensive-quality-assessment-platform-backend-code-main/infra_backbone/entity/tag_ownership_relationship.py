"""
标签所属关系 实体类
"""
from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, Index, String

from infra_backbone.entity.history.tag_ownership_relationship_history import (
    TagOwnershipRelationshipHistoryEntity,
)


class TagOwnershipRelationshipEntity(VersionedEntity):
    """
    标签所属关系
    """

    __tablename__ = "st_tag_ownership_relationship"
    __table_args__ = {"comment": "标签所属关系"}
    __history_entity__ = TagOwnershipRelationshipHistoryEntity

    tag_ownership_id = Column(String(40), nullable=False, comment="标签所属id", index=True)
    resource_category = Column(String(255), nullable=False, comment="资源类型")
    resource_id = Column(String(40), nullable=False, comment="资源id")
    relationship = Column(String(255), nullable=False, comment="关系", index=True)


Index(
    "idx_tag_ownership_relationship_resource_info",
    TagOwnershipRelationshipEntity.resource_category,
    TagOwnershipRelationshipEntity.resource_id,
)
