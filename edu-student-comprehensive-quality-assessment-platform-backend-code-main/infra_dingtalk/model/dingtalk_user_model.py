from datetime import datetime
from typing import Dict, List, Optional

from infra_basic.basic_model import VersionedModel

from infra_dingtalk.model.view.dingtalk_dept_user_duty_vm import DingtalkDeptUserDutyViewModel
from infra_dingtalk.model.view.dingtalk_user_k12_dept_duty_vm import (
    DingtalkUserK12DeptDutyViewModel,
)


class DingtalkUserModel(VersionedModel):
    """
    钉钉用户
    """

    dingtalk_corp_id: str
    remote_user_id: str
    unionid: str
    name: str
    avatar: Optional[str]
    state_code: Optional[str]
    mobile: Optional[str]
    hide_mobile: Optional[bool] = False
    telephone: Optional[str]
    job_number: Optional[str]
    email: Optional[str]
    org_email: Optional[str]
    work_place: Optional[str]
    extension: Optional[Dict]
    hired_date: Optional[datetime]
    admin: Optional[bool] = False
    boss: Optional[bool] = False

    remote_dept_ids: List[int] = []
    dingtalk_dept_user_duty_list: List[DingtalkDeptUserDutyViewModel] = []
    dingtalk_k12_dept_user_duty_list: List[DingtalkUserK12DeptDutyViewModel] = []

    def unique_dict(self) -> Dict:
        """
        获取判断唯一性的字典
        """
        unique_cols = [
            "name",
            "avatar",
            "state_code",
            "mobile",
            "hide_mobile",
            "telephone",
            "job_number",
            "thumb_avatar",
            "email",
            "org_email",
            "work_place",
            "extension",
            "admin",
            "boss",
        ]
        data = {}
        for col in unique_cols:
            value = self.dict().get(col)
            if value == "":
                value = None
            data[col] = value
        return data

    def empty_to_none(self):
        """
        空字符串转None
        """
        for k, v in self.dict().items():
            if v == "":
                setattr(self, k, None)
