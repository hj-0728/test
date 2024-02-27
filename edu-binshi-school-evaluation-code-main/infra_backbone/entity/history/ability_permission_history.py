from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class AbilityPermissionHistoryEntity(HistoryEntity):
    """
    功能权限历史
    """

    __tablename__ = "st_ability_permission_history"
    __table_args__ = {"comment": "功能权限历史"}
    name = Column(String(255), nullable=False, comment="名称")
    code = Column(String(255), comment="编码", nullable=False)


# 时间检索索引
Index(
    "idx_ability_permission_history_time_range",
    AbilityPermissionHistoryEntity.id,
    AbilityPermissionHistoryEntity.begin_at,
    AbilityPermissionHistoryEntity.end_at.desc(),
    unique=True,
)
