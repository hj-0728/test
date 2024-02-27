"""
钉钉k12的部门及部门负责人
"""

from typing import Dict, List, Optional

from infra_basic.basic_model import BasePlusModel

from infra_dingtalk.model.dingtalk_user_k12_dept_duty_model import DingtalkUserK12DeptDutyModel


class DingtalkK12DeptWithAdminsViewModel(BasePlusModel):
    """
    钉钉k12的部门及部门负责人
    """

    id: str
    version: int
    dingtalk_corp_id: str
    name: str
    remote_dept_id: int
    parent_dingtalk_k12_dept_id: Optional[str]
    parent_remote_dept_id: Optional[int]
    contact_type: str
    dept_type: str
    feature: Optional[str]
    nick: Optional[str]
    seq: Optional[int]

    admins: List[DingtalkUserK12DeptDutyModel] = []

    def unique_dict(self) -> Dict:
        """
        获取用于判断唯一性的字典，用于判断数据是否改变
        """
        if self.parent_remote_dept_id:
            parent_remote_id = self.parent_remote_dept_id
        else:
            parent_remote_id = 0
        return {
            "contact_type": self.contact_type,
            "name": self.name,
            "parent_id": parent_remote_id,
            "dept_type": self.dept_type,
            "feature": self.feature,
            "nick": self.nick,
        }
