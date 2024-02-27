from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, Index, String

from infra_backbone.entity.history.resource_contact_info_history import (
    ResourceContactInfoHistoryEntity,
)


class ResourceContactInfoEntity(VersionedEntity):
    """
    资源联系方式
    """

    __tablename__ = "st_resource_contact_info"
    __table_args__ = {"comment": "资源联系方式"}
    __history_entity__ = ResourceContactInfoHistoryEntity

    resource_category = Column(String(255), nullable=False, comment="资源类型")
    resource_id = Column(String(40), nullable=False, comment="资源id")
    contact_info_id = Column(String(40), nullable=False, comment="联系方式id", index=True)


Index(
    "idx_resource_contact_info_resource_info",
    ResourceContactInfoEntity.resource_category,
    ResourceContactInfoEntity.resource_id,
)
