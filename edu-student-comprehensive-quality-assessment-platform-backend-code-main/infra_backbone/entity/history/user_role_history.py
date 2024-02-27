from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class UserRoleHistoryEntity(HistoryEntity):
    """
    用户角色历史
    """

    __tablename__ = "st_user_role_history"
    __table_args__ = {"comment": "用户角色历史"}

    user_id = Column(String(40), nullable=False, comment="用户id", index=True)
    role_id = Column(String(40), nullable=False, comment="角色id", index=True)


Index(
    "idx_user_role_history_time_range",
    UserRoleHistoryEntity.id,
    UserRoleHistoryEntity.commenced_on,
    UserRoleHistoryEntity.ceased_on.desc(),
    unique=True,
)
