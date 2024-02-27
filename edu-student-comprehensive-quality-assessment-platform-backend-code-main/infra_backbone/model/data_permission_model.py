"""
数据权限
"""
from datetime import datetime
from enum import Enum
from typing import List, Optional

from infra_basic.basic_model import VersionedModel


class DataPermissionDetailModel(VersionedModel):
    """
    数据权限 详情
    """

    data_permission_id: str
    object_id: str
    object_category: str
    started_on: datetime
    ended_on: Optional[datetime]


class DataPermissionModel(VersionedModel):
    """
    数据权限
    """

    subject_category: str
    subject_id: str
    aspect: str
    policy: str
    detail_list: List[DataPermissionDetailModel] = []


class EnumDataPermissionSubjectCategory(Enum):
    """
    主资源类别
    """

    USER_ROLE = "用户角色"
    ORGANIZATION = "组织"


class EnumDataPermissionObjectCategory(Enum):
    """
    对象类型
    """

    ORGANIZATION = "组织"


class EnumDataPermissionAspect(Enum):
    """
    轴
    """

    MANAGE_SCHOOL = "管理的学校"
    OPERATIONAL_SCHOOL = "可操作的学校"


class EnumDataPermissionPolicy(Enum):
    """
    策略:允许/拒绝
    """

    ALLOW = "允许"
    REFUSE = "拒绝"
