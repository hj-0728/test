from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, Integer, String


class AbilityPermissionTreeHistoryEntity(HistoryEntity):
    """
    功能权限树历史
    """

    __tablename__ = "st_ability_permission_tree_history"
    __table_args__ = {"comment": "功能权限树历史"}

    ability_permission_group_id = Column(String(40), nullable=True, comment="分组id，空的话为根节点")
    child_resource_category = Column(String(255), nullable=False, comment="子资源类别")
    child_resource_id = Column(String(40), nullable=False, comment="子资源id")
    seq = Column(Integer, nullable=True, comment="排序")


# 时间检索索引
Index(
    "idx_ability_permission_tree_history_time_range",
    AbilityPermissionTreeHistoryEntity.id,
    AbilityPermissionTreeHistoryEntity.begin_at,
    AbilityPermissionTreeHistoryEntity.end_at.desc(),
    unique=True,
)
