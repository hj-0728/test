"""
钉钉部门用户职责
"""

from typing import Optional

from infra_basic.basic_model import BasePlusModel


class DingtalkDeptUserDutyViewModel(BasePlusModel):
    """
    钉钉部门用户职责
    """

    id: str
    remote_dept_id: Optional[int]
    duty: str
    dingtalk_dept_id: Optional[str]
    seq: int
    version: int


class DingtalkDeptUserDutyVm(BasePlusModel):
    """
    钉钉部门用户职责
    """

    dingtalk_user_id: str
    duty: str
