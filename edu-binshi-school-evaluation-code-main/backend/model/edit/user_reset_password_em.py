from enum import Enum

from infra_backbone.model.user_model import UserModel


class EnumUserType(Enum):
    """
    钉钉用户类型
    """

    STUDENT = "学生"
    TEACHER = "老师"


class UserResetPasswordEditModel(UserModel):
    user_type: str
