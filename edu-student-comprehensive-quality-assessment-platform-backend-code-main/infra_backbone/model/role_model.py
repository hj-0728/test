"""
角色
"""
from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel


class EnumRoleCode(str, Enum):
    """
    角色 code
    """

    SYSTEM_ADMIN = "系统管理员"
    ADMIN = "管理员"
    TEACHER = "教师"
    STUDENT = "学生"


class RoleModel(VersionedModel):
    """
    角色信息
    """

    name: Optional[str]
    code: Optional[str]
    comments: Optional[str]
    user_role_id: Optional[str]
    is_activated: bool = True
