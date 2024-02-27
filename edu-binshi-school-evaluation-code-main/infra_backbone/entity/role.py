from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Boolean, Column, String

from infra_backbone.entity.history.role_history import RoleHistoryEntity


class RoleEntity(VersionedEntity):
    """
    角色
    """

    __tablename__ = "st_role"
    __table_args__ = {"comment": "角色"}
    __history_entity__ = RoleHistoryEntity

    name = Column(String(255), nullable=False, comment="名称")
    code = Column(String(255), nullable=False, comment="编码", index=True, unique=True)
    comments = Column(String(2000), nullable=True, comment="描述")
    is_activated = Column(Boolean, nullable=False, comment="是否激活")
