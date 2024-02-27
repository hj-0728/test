from typing import List, Optional

from infra_basic.basic_model import BasicModel, VersionedModel


class UserRoleModel(VersionedModel):
    """
    用户角色信息
    """

    user_id: Optional[str]
    role_id: Optional[str]
    role_code: Optional[str]


class SaveUserRoleModel(BasicModel):
    user_id: str
    role_id_list: List[str]
