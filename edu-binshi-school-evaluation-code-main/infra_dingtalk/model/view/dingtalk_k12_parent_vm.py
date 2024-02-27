"""
企微k12家长
"""
from typing import Optional

from infra_utility.base_plus_model import BasePlusModel


class DingtalkK12ParentViewModel(BasePlusModel):
    """
    钉钉k12家长
    """

    id: str
    dingtalk_corp_id: str
    remote_user_id: str
    name: Optional[str]
    mobile: Optional[str]
