from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel


class EnumDingtalkK12DeptCategory(Enum):
    """
    部门类型
    """

    ROOT = "根"
    CAMPUS = "校区"
    ACADEMIC_SECTION = "学段"
    GRADE = "年级"
    SCHOOL_CLASS = "班级"


class EnumDingtalkK12DeptCategoryMap(Enum):
    """
    1表示班级，2表示年级，3表示学段，4表示校区，5表示学校（根部门）
    """

    ROOT = 5
    CAMPUS = 4
    ACADEMIC_SECTION = 3
    GRADE = 2
    SCHOOL_CLASS = 1


class EnumDingtalkK12DeptType(Enum):
    """
    部门类型
    """

    CAMPUS = "校区"
    PERIOD = "学段"
    GRADE = "年级"
    CLASS = "班级"
    DEPT = "自定义部门"  # 普通节点，没有业务含义，主要用于自定义通讯录中


class DingtalkK12DeptModel(VersionedModel):
    """
    钉钉 k12 部门
    """

    dingtalk_corp_id: str
    name: str
    remote_dept_id: str
    parent_dingtalk_k12_dept_id: Optional[str]
    parent_remote_dept_id: Optional[int]
    contact_type: str
    dept_type: str
    feature: Optional[str]
    nick: Optional[str]
