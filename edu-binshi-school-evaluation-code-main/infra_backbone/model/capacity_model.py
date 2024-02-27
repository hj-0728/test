from enum import Enum

from infra_basic.basic_model import VersionedModel


class EnumCapacityCode(Enum):
    """
    容量编码
    """

    TEACHER = "任课老师"
    HEAD_TEACHER = "班主任"
    STUDENT = "学生"
    LEADER = "领导"
    MEMBER = "成员"
    PARENT = "家长"


class CapacityModel(VersionedModel):
    name: str
    code: str
    is_available: bool = True
