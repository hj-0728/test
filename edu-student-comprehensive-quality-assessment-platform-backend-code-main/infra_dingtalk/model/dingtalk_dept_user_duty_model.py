from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel


class EnumDingtalkUserDuty(Enum):
    """
    钉钉用户职责
    """

    MEMBER = "成员"
    LEADER = "领导"


class DingtalkDeptUserDutyModel(VersionedModel):
    """
    钉钉部门用户职责
    """

    dingtalk_user_id: Optional[str]
    dingtalk_dept_id: Optional[str]
    duty: str
    seq: int = 1
