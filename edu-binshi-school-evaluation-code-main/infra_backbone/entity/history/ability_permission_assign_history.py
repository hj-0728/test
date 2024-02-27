from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class AbilityPermissionAssignHistoryEntity(HistoryEntity):
    """
    功能权限授予历史
    """

    __tablename__ = "st_ability_permission_assign_history"
    __table_args__ = {"comment": "功能权限授予历史"}

    ability_permission_id = Column(String(40), nullable=False, comment="功能权限id")
    assign_resource_category = Column(String(255), nullable=False, comment="授予资源类别")
    assign_resource_id = Column(String(40), nullable=False, comment="授予资源id")


# 时间检索索引
Index(
    "idx_ability_permission_assign_history_time_range",
    AbilityPermissionAssignHistoryEntity.id,
    AbilityPermissionAssignHistoryEntity.begin_at,
    AbilityPermissionAssignHistoryEntity.end_at.desc(),
    unique=True,
)
