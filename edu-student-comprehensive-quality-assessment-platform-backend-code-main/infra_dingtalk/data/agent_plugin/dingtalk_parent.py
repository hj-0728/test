"""
家长
"""

from typing import Dict, Optional

from infra_basic.basic_model import BasePlusModel

from infra_dingtalk.model.dingtalk_k12_family_relationship_model import (
    DingtalkK12FamilyRelationshipModel,
)
from infra_dingtalk.model.dingtalk_k12_parent_model import DingtalkK12ParentModel


class DingtalkParent(BasePlusModel):
    """
    家长
    """

    from_userid: str
    relation_name: str
    relation_code: str
    mobile: Optional[str]
    unionid: str
    feature: Optional[Dict]

    def to_family_relationship_em(
        self, student_id: str, parent_id: str
    ) -> DingtalkK12FamilyRelationshipModel:
        return DingtalkK12FamilyRelationshipModel(
            dingtalk_k12_student_id=student_id,
            dingtalk_k12_parent_id=parent_id,
            relationship_code=self.relation_code,
            relationship_name=self.relation_name,
        )

    def to_dingtalk_k12_parent_em(self, dingtalk_corp_id: str) -> DingtalkK12ParentModel:
        return DingtalkK12ParentModel(
            dingtalk_corp_id=dingtalk_corp_id,
            remote_user_id=self.from_userid,
            mobile=self.mobile,
            unionid=self.unionid,
            feature=self.feature,
        )

    def unique_dict(self) -> Dict:
        """
        获取判断唯一性的字典
        """

        return {
            "parent_userid": self.from_userid,
            "mobile": self.mobile,
            "unionid": self.unionid,
            "feature": self.feature,
        }
