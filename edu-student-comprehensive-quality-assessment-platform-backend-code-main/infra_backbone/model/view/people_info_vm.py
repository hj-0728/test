"""
人员信息
"""

from typing import List, Optional

from infra_basic.basic_model import BasicModel
from pydantic import BaseModel


class NumberInfoOfPeopleInfo(BaseModel):
    """
    人员信息的身份编号信息
    """

    category: str
    category_display: Optional[str]
    number: str


class PeopleInfoVm(BasicModel):
    """
    人员信息
    """

    id: str
    name: str
    gender: str
    gender_display: Optional[str]
    born_on: Optional[str]
    is_verified: Optional[bool]
    phone_list: List[str] = []
    number_info: List[NumberInfoOfPeopleInfo] = []
