"""
企微k12家长
"""
from typing import Dict, Optional

from infra_basic.basic_model import VersionedModel


class DingtalkK12ParentModel(VersionedModel):
    """
    企微k12家长
    """

    dingtalk_corp_id: str
    remote_user_id: str
    mobile: Optional[str]
    unionid: str
    feature: Optional[Dict]

    def unique_dict(self) -> Dict:
        """
        获取判断唯一性的字典
        """

        return {
            "parent_userid": self.remote_user_id,
            "mobile": self.mobile,
            "unionid": self.unionid,
            "feature": self.feature,
        }
