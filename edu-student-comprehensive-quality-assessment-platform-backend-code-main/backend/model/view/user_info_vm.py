from typing import List

from infra_basic.basic_model import BasePlusModel

from infra_backbone.model.role_model import RoleModel


class UserInfoViewModel(BasePlusModel):
    id: str
    name: str
    role_list: List[RoleModel]
    current_role: RoleModel
