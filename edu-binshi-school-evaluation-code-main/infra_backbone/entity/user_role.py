from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String, UniqueConstraint

from infra_backbone.entity.history.user_role_history import UserRoleHistoryEntity


class UserRoleEntity(VersionedEntity):
    """
    用户角色
    """

    __tablename__ = "st_user_role"

    __table_args__ = (
        UniqueConstraint("user_id", "role_id", name="uc_user_role_user_id_role_id"),
        {"comment": "用户角色"},
    )
    __history_entity__ = UserRoleHistoryEntity

    user_id = Column(String(40), nullable=False, comment="用户id", index=True)
    role_id = Column(String(40), nullable=False, comment="角色id", index=True)
