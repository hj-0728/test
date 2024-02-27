from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel


class EnumChildResourceCategory(str, Enum):
    ABILITY_PERMISSION_GROUP = "功能权限分组"
    ABILITY_PERMISSION = "功能权限"


class AbilityPermissionTreeModel(VersionedModel):
    ability_permission_group_id: Optional[str]
    child_resource_category: str
    child_resource_id: str
    seq: int
