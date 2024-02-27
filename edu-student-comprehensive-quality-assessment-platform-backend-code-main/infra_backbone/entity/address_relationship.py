from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, Index, String

from infra_backbone.entity.history.address_relationship_history import (
    AddressRelationshipHistoryEntity,
)


class AddressRelationshipEntity(VersionedEntity):
    """
    地址关联
    """

    __tablename__ = "st_address_relationship"
    __table_args__ = {"comment": "地址关联"}
    __history_entity__ = AddressRelationshipHistoryEntity

    address_id = Column(String(40), nullable=False, comment="地址id", index=True)
    resource_category = Column(String(255), nullable=False, comment="资源类别")
    resource_id = Column(String(40), nullable=False, comment="资源id")
    relationship = Column(String(255), nullable=False, comment="关系", index=True)


Index(
    "idx_address_relationship_resource_info",
    AddressRelationshipEntity.resource_category,
    AddressRelationshipEntity.resource_id,
)
