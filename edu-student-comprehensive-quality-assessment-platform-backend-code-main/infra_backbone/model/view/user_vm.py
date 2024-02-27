from typing import List, Optional

from infra_basic.basic_model import BasicModel

from infra_backbone.model.role_model import RoleModel


class UserViewModel(BasicModel):
    name: str
    is_activated: bool
    password_reset: bool
    home_path: Optional[str]

    current_role: Optional[RoleModel]
    role_list: List[RoleModel] = []
