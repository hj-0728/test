from infra_basic.basic_model import BaseModel


class UserRoleProfileViewModel(BaseModel):
    """
    用户角色信息
    """

    user_id: str
    role_id: str
    role_code: str
