from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel


class EnumMenuOpenMethod(Enum):
    """
    菜单打开方式
    """

    CURRENT = "当前窗口"
    NEW = "新窗口"


class EnumMenuCategory(Enum):
    """
    菜单的category
    """

    WEB = "web"
    MOBILE = "mobile"


class MenuModel(VersionedModel):
    """
    菜单
    """

    name: Optional[str]
    code: Optional[str]
    path: Optional[str]
    icon: Optional[str]
    parent_id: Optional[str]
    outline: Optional[str]
    open_method: str = EnumMenuOpenMethod.CURRENT.name
    category: str = EnumMenuCategory.WEB.name
    seq: int = 1
