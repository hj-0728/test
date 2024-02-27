from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class AbilityPermissionGroupHistoryEntity(HistoryEntity):
    """
    功能权限分组历史
    """

    __tablename__ = "st_ability_permission_group_history"
    __table_args__ = {"comment": "功能权限分组历史"}

    name = Column(String(255), nullable=False, comment="名称")
    code = Column(String(255), nullable=False, comment="编码")


# 时间检索索引
Index(
    "idx_ability_permission_group_history_time_range",
    AbilityPermissionGroupHistoryEntity.id,
    AbilityPermissionGroupHistoryEntity.commenced_on,
    AbilityPermissionGroupHistoryEntity.ceased_on.desc(),
    unique=True,
)
