from typing import Optional

from infra_basic.basic_model import BasePlusModel


class UserProfileViewModel(BasePlusModel):
    """
    用户信息
    """

    role_id: str
    role_code: str
    user_id: Optional[str]
