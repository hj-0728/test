from enum import Enum
from typing import Optional

from infra_basic.basic_model import BasePlusModel
from infra_basic.errors import BusinessError


class EnumOauthUserCategory(Enum):
    DINGTALK_USER = "钉钉用户"
    DINGTALK_K12_PARENT = "钉钉家长"


class OauthResultViewModel(BasePlusModel):
    """
    钉钉 oauth2.0 回调结果
    """

    remote_user_id: str
    user_category: str
    dingtalk_user_id: Optional[str]
    dingtalk_k12_parent_id: Optional[str]
    dingtalk_corp_id: str

    def get_user_id(self) -> str:
        """
        获取用户id
        :return:
        """
        if self.dingtalk_user_id:
            return self.dingtalk_user_id
        if self.dingtalk_k12_parent_id:
            return self.dingtalk_k12_parent_id
        raise BusinessError("未获取到用户id")
