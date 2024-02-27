from typing import Optional

from infra_basic.basic_model import VersionedModel

from infra_backbone.model.ability_permission_group_model import AbilityPermissionGroupModel
from infra_backbone.model.ability_permission_model import AbilityPermissionModel


class AbilityPermissionEditModel(VersionedModel):
    """
    功能权限
    """

    name: Optional[str]
    code: Optional[str]
    parent_id: Optional[str]
    is_permission: bool = False
    node_type: Optional[str]
    seq: int = 1
    tree_id: Optional[str]
    tree_version: Optional[int]

    def to_ability_permission_model(self):
        if self.id:
            return AbilityPermissionModel(
                id=self.id,
                name=self.name,
                code=self.code,
            )
        return AbilityPermissionModel(
            name=self.name,
            code=self.code,
        )

    def to_ability_permission_group_model(self):
        if self.id:
            return AbilityPermissionGroupModel(
                id=self.id,
                name=self.name,
                code=self.code,
            )
        return AbilityPermissionGroupModel(
            name=self.name,
            code=self.code,
        )
