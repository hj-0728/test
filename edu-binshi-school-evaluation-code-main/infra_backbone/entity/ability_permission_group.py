from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from infra_backbone.entity.history.ability_permission_group_history import (
    AbilityPermissionGroupHistoryEntity,
)


class AbilityPermissionGroupEntity(VersionedEntity):
    """
    功能权限分组
    """

    __tablename__ = "st_ability_permission_group"
    __table_args__ = {"comment": "功能权限分组"}
    __history_entity__ = AbilityPermissionGroupHistoryEntity

    name = Column(String(255), nullable=False, comment="名称")
    code = Column(String(255), nullable=False, comment="编码", index=True, unique=True)
