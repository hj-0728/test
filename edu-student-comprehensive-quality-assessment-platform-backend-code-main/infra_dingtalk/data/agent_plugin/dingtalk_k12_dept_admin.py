"""
家校通讯录k12部门里的负责人
"""


from typing import Optional

from infra_basic.basic_model import BasePlusModel
from infra_utility.enum_helper import get_enum_name_by_value

from infra_dingtalk.model.dingtalk_user_k12_dept_duty_model import (
    DingtalkUserK12DeptDutyModel,
    EnumDingtalkUserK12DeptDutyMap,
)


class DingtalkK12DeptAdmin(BasePlusModel):
    """
    家校通讯录k12部门里的负责人
    """

    userid: str
    duty: str
    subject: Optional[str]

    def to_dingtalk_user_k12_dept_duty_em(
        self, dingtalk_user_id: str, dingtalk_k12_dept_id: str
    ) -> DingtalkUserK12DeptDutyModel:
        return DingtalkUserK12DeptDutyModel(
            dingtalk_user_id=dingtalk_user_id,
            dingtalk_k12_dept_id=dingtalk_k12_dept_id,
            duty=self.duty,
        )

    def get_dingtalk_user_duty(self) -> str:
        """
        获取职责
        """
        return get_enum_name_by_value(
            enum_class=EnumDingtalkUserK12DeptDutyMap, enum_value=self.type
        )
