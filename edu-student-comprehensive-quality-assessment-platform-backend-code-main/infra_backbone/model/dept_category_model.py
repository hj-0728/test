from enum import Enum

from infra_basic.basic_model import VersionedModel


class EnumDeptCategoryCode(Enum):
    """
    部门类型code枚举
    """

    CAMPUS = "校区"
    PERIOD = "学段"
    GRADE = "年级"
    CLASS = "班级"
    DEPT = "自定义部门"


class DeptCategoryModel(VersionedModel):
    organization_id: str
    name: str
    code: str
    is_activated: bool = True
