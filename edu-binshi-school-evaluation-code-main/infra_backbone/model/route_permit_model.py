from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel


class RoutePermitModel(VersionedModel):
    route_id: Optional[str]
    permitted_resource_category: str
    permitted_resource_id: Optional[str]


class EnumRoutePermitResourceCategory(Enum):
    """
    路由权限所属资源
    """

    ROLE = "角色"
    ABILITY_PERMISSION = "功能权限"
