from infra_basic.basic_model import BasePlusModel


class UserPasswordEditModel(BasePlusModel):
    """
    用户密码
    """

    password: str
    new_password: str
    verify_new_password: str


class ImproveUserPasswordEditModel(BasePlusModel):
    """
    完善用户密码
    """

    new_password: str
    verify_new_password: str
