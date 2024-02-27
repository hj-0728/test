from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from infra_basic.basic_model import VersionedModel

from infra_dingtalk.model.view.dingtalk_dept_user_duty_vm import DingtalkDeptUserDutyViewModel
from infra_dingtalk.model.view.dingtalk_user_k12_dept_duty_vm import (
    DingtalkUserK12DeptDutyViewModel,
)


class EnumDingtalkUserGenderMap(Enum):
    """
    钉钉用户性别与数据库字段关联
    """

    UNDEFINED = 0
    MALE = 1
    FEMALE = 2


class EnumDingtalkUserStatusMap(Enum):
    """
    钉钉用户状态与数据库字段关联
    """

    ACTIVATED = 1
    DISABLED = 2
    INACTIVATED = 4
    QUITTED = 5


class EnumDingtalkUserCategory(Enum):
    """
    钉钉用户类型
    """

    dingtalk_USER = "钉钉用户"
    dingtalk_K12_PARENT = "钉钉K12家长"


class EnumDingtalkUserStatus(Enum):
    """
    钉钉用户状态
    1=已激活，2=已禁用，4=未激活，5=退出企业。
    """

    ACTIVATED = "已激活"
    DISABLED = "已禁用"
    INACTIVATED = "未激活"
    QUITTED = "退出企业"


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
            data[col] = value
        return data
