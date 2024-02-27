"""
钉钉 获取访问用户身份
"""
from typing import Optional

from infra_basic.basic_model import BasePlusModel
from pydantic import Field


class DingtalkUserInfo(BasePlusModel):
    """
    钉钉 获取访问用户身份

    sys: 是否是系统管理员
    true：是
    false：不是

    sys_level: 系统管理员级别
    1：主管理员
    2：子管理员
    100：老板
    0：其他（如普通员工）
    """

    user_id: str = Field(..., alias="userid")
    device_id: str
    sys: bool
    sys_level: int
    associated_union_id: Optional[str] = Field(None, alias="associated_unionid")
    union_id: Optional[str] = Field(None, alias="unionid")
    name: str
