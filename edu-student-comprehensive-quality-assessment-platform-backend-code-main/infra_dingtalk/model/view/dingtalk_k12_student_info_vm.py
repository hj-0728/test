"""
企微k12家长
"""
from typing import List, Optional

from infra_utility.base_plus_model import BasePlusModel


class DingtalkK12StudentFamilyViewModel(BasePlusModel):
    parent_id: Optional[str]
    relationship_name: Optional[str]


class DingtalkK12StudentInfoViewModel(BasePlusModel):
    """
    企微k12家长
    """

    id: str
    dingtalk_corp_id: str
    name: str
    remote_user_id: str
    dingtalk_k12_dept_id_list: List[str]
    family_relationship: List[DingtalkK12StudentFamilyViewModel]
