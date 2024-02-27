from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, Index, String

from infra_backbone.entity.history.ability_permission_assign_history import (
    AbilityPermissionAssignHistoryEntity,
)


class AbilityPermissionAssignEntity(VersionedEntity):
    """
    功能权限授予
    """

    __tablename__ = "st_ability_permission_assign"
    __table_args__ = {"comment": "功能权限授予"}
    __history_entity__ = AbilityPermissionAssignHistoryEntity

    ability_permission_id = Column(String(40), nullable=False, comment="功能权限id", index=True)
    assign_resource_category = Column(String(255), nullable=True, comment="授予资源类别")
    assign_resource_id = Column(String(40), nullable=True, comment="授予资源id")


Index(
    "idx_ability_permission_assign_resource_info",
    AbilityPermissionAssignEntity.assign_resource_category,
    AbilityPermissionAssignEntity.assign_resource_id,
)
