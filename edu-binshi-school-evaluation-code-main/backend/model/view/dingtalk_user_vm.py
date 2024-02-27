"""
钉钉用户信息
"""

from typing import Optional

from infra_basic.basic_model import BaseModel
from infra_basic.resource_interface import Resource

from backend.data.enum import EnumDingtalkUserCategory


class DingtalkUserVm(BaseModel, Resource):
    """
    钉钉用户信息
    """

    dingtalk_corp_id: str
    user_category: str
    dingtalk_user_id: Optional[str]
    remote_user_id: Optional[str]
    dingtalk_k12_parent_id: Optional[str]
    capacity_id: Optional[str]
    capacity_code: Optional[str]

    def res_category(self):
        """
        获取资源类型
        :return:
        """
        return self.user_category

    def res_id(self):
        """
        获取资源类型
        :return:
        """
        if self.user_category == EnumDingtalkUserCategory.DINGTALK_USER.name:
            return self.dingtalk_user_id
        return self.dingtalk_k12_parent_id
