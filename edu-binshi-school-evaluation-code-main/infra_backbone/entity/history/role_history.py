"""
角色  历史实体类
"""
from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Boolean, Column, Index, String


class RoleHistoryEntity(HistoryEntity):
    """
    角色历史
    """

    __tablename__ = "st_role_history"
    __table_args__ = {"comment": "角色历史"}

    name = Column(String(255), nullable=False, comment="名称")
    code = Column(String(255), nullable=False, comment="编码")
    comments = Column(String(2000), nullable=True, comment="描述")
    is_activated = Column(Boolean, nullable=False, comment="是否激活")


Index(
    "idx_role_history_time_range",
    RoleHistoryEntity.id,
    RoleHistoryEntity.begin_at,
    RoleHistoryEntity.end_at.desc(),
    unique=True,
)
