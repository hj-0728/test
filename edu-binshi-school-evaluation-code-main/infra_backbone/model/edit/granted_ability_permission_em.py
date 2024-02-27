"""
被功能权限授权的对象em
"""

from typing import List

from infra_basic.basic_model import VersionedModel

from infra_backbone.model.ability_permission_assign_model import AbilityPermissionAssignModel


class AbilityPermissionAssignEm(VersionedModel):
    """
    被功能权限授权的对象em
    """

    assign_resource_category: str
    assign_resource_id: str
    ability_permission_id_list: List[str] = []

    def to_ability_permission_assign_model(self, ability_permission_id: str):
        """
        转化
        """
        return AbilityPermissionAssignModel(
            ability_permission_id=ability_permission_id,
            assign_resource_category=self.assign_resource_category,
            assign_resource_id=self.assign_resource_id,
        )
