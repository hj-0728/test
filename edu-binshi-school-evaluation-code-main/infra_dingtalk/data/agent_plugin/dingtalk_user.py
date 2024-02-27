from datetime import datetime
from typing import Dict, List, Optional

from infra_basic.basic_model import BasePlusModel
from infra_utility.enum_helper import get_enum_name_by_value

from infra_dingtalk.model.dingtalk_dept_user_duty_model import EnumDingtalkUserDuty
from infra_dingtalk.model.dingtalk_user_model import (
    DingtalkUserModel,
    EnumDingtalkUserGenderMap,
    EnumDingtalkUserStatusMap,
)


class DingtalkUser(BasePlusModel):
    """
    企业微信接口里面返回的企业微信用户信息
    """

    userid: str
    unionid: str
    name: str
    is_leader_in_depts: Optional[str]
    boss: bool
    hide_mobile: bool
    hired_date: Optional[datetime]
    telephone: Optional[str]
    department: List[int] = []
    work_place: Optional[str]
    email: Optional[str]
    order_in_depts: Optional[str]
    mobile: Optional[str]
    avatar: Optional[str]
    admin: bool
    extattr: Optional[Dict]
    state_code: Optional[str]
    position: Optional[str]
    is_leader_in_dept: List[int] = []

    def to_dingtalk_user_em(self, dingtalk_corp_id: str) -> DingtalkUserModel:
        data = self.dict()
        data["remote_user_id"] = self.userid
        data["dingtalk_corp_id"] = dingtalk_corp_id
        return DingtalkUserModel(**data)

    def unique_dict(self) -> Dict:
        """
        获取md5值
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

    def get_dept_duty(self, remote_dept_id: int) -> str:
        """
        获取在部门中的职责
        """
        if remote_dept_id in self.is_leader_in_dept:
            return EnumDingtalkUserDuty.LEADER.name
        return EnumDingtalkUserDuty.MEMBER.name

    def get_map_gender(self) -> str:
        """
        获取映射后的性别值
        """
        return get_enum_name_by_value(enum_class=EnumDingtalkUserGenderMap, enum_value=self.gender)

    def get_map_status(self) -> str:
        """
        获取映射后的状态值
        """
        return get_enum_name_by_value(enum_class=EnumDingtalkUserStatusMap, enum_value=self.status)
