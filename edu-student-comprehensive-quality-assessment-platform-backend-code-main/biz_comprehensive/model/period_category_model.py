"""
周期类型
"""
from enum import Enum

from infra_basic.basic_model import VersionedModel


class EnumPeriodCategoryCode(Enum):
    """
    周期类型 code
    """

    ACADEMIC_YEAR = "学年"
    SEMESTER = "学期"
    WEEK = "周"
    MONTH = "月"


class PeriodCategoryModel(VersionedModel):
    """
    周期类型
    """

    name: str
    code: str
