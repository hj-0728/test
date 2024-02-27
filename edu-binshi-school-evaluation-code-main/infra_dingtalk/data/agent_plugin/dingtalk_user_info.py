"""
钉钉 获取访问用户身份
"""
from typing import Optional

from infra_basic.basic_model import BasePlusModel
from pydantic import Field


class DingtalkUserInfo(BasePlusModel):
    """
    钉钉 获取访问用户身份
    """

    err_code: int = Field(None, alias="errcode")
    err_msg: str = Field(None, alias="errmsg")
    user_id: Optional[str] = Field(None, alias="userid")
    device_id: str = Field(None, alias="deviceId")
