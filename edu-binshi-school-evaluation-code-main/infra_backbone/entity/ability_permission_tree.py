from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, Index, Integer, String, text

from infra_backbone.entity.history.ability_permission_tree_history import (
    AbilityPermissionTreeHistoryEntity,
)


class AbilityPermissionTreeEntity(VersionedEntity):
    """
    功能权限树
    """

    __tablename__ = "st_ability_permission_tree"
    __table_args__ = {"comment": "功能权限树"}
    __history_entity__ = AbilityPermissionTreeHistoryEntity

    ability_permission_group_id = Column(
        String(40), nullable=True, comment="分组id，空的话为根节点", index=True
    )
    child_resource_category = Column(String(255), nullable=False, comment="子资源类别")
    child_resource_id = Column(String(40), nullable=False, comment="子资源id")
    seq = Column(Integer, nullable=False, comment="排序", server_default=text("1"))


Index(
    "idx_ability_permission_tree_resource_info",
    AbilityPermissionTreeEntity.child_resource_category,
    AbilityPermissionTreeEntity.child_resource_id,
)
