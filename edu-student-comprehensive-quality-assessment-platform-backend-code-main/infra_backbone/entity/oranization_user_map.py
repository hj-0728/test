from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from infra_backbone.entity.history.organization_user_map_history import (
    OrganizationUserMapHistoryEntity,
)


class OrganizationUserMapEntity(VersionedEntity):
    """
    组织用户map 实体类
    """

    __tablename__ = "st_organization_user_map"
    __table_args__ = {"comment": "组织用户map"}
    __history_entity__ = OrganizationUserMapHistoryEntity

    organization_id = Column(String(40), nullable=False, comment="组织id", index=True)
    user_id = Column(String(40), nullable=False, comment="用户id", index=True)
