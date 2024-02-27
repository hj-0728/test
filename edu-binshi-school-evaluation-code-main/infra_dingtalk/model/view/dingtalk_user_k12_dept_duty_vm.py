"""
钉钉部门用户职责
"""

from typing import Optional

from infra_basic.basic_model import BasePlusModel


class DingtalkUserK12DeptDutyViewModel(BasePlusModel):
    """
    钉钉部门用户职责
    """

    id: str
    remote_dept_id: Optional[int]
    duty: str
    dingtalk_k12_dept_id: Optional[str]
    version: int
