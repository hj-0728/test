from typing import Optional

from infra_basic.basic_model import BaseModel
from infra_basic.resource_interface import Resource


class UserProfileViewModel(BaseModel, Resource):
    """
    用户信息
    """

    user_category: str
    user_id: str
    people_id: Optional[str]

    def res_category(self) -> str:
        """
        获取资源类型
        :return:
        """
        return self.user_category

    def res_id(self) -> str:
        """
        获取资源类型
        :return:
        """
        return self.user_id
