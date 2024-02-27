from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel
from infra_utility.algorithm.tree import TreeNodeModel


class EnumAbilityPermissionAssignResourceCategory(Enum):
    """
    被功能权限授权的对象类型
    """

    ROLE = "角色"
    MENU = "菜单"


class AbilityPermissionAssignModel(VersionedModel):
    ability_permission_id: str
    assign_resource_category: str
    assign_resource_id: str


class AbilityPermissionAssignTreeViewModel(TreeNodeModel):
    """
    授权功能权限树
    """

    id: str
    parent_id: Optional[str]
    name: Optional[str]
    code: Optional[str]
    granted: Optional[bool]
    node_type: str
    tree_seq: int
