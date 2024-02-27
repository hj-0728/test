from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from infra_backbone.entity.history.ability_permission_history import AbilityPermissionHistoryEntity


class AbilityPermissionEntity(VersionedEntity):
    """
    功能权限
    """

    __tablename__ = "st_ability_permission"
    __table_args__ = {"comment": "功能权限"}
    __history_entity__ = AbilityPermissionHistoryEntity
    name = Column(String(255), nullable=False, comment="名称")
    code = Column(String(255), comment="编码", nullable=False, index=True, unique=True)
