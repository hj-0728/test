"""
人员列表
"""

from typing import List, Optional

from infra_basic.basic_model import BasicModel
from infra_utility.base_plus_model import BasePlusModel


class DeptOfPeoplePageVm(BasePlusModel):
    establishment_id: str
    name: str


class PeoplePageVm(BasicModel):
    """
    人员列表
    """

    name: str
    gender: Optional[str]
    gender_display: Optional[str]
    dept_list: List[DeptOfPeoplePageVm]

    dept: Optional[str]
