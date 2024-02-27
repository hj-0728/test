"""
人员
"""

from typing import List, Optional

from infra_basic.basic_model import BasePlusModel


class PeopleEm(BasePlusModel):
    """
    人员
    """

    name: str
    gender: str
    identity_category: Optional[str]
    identity_number: Optional[str]
    mobile_list: List[str]
