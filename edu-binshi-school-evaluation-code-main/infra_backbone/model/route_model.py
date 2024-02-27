from enum import Enum
from typing import List, Optional

from infra_basic.basic_model import VersionedModel

from infra_backbone.model.edit.route_permit_em import RoutePermitEditModel
from infra_backbone.model.route_permit_model import (
    EnumRoutePermitResourceCategory,
    RoutePermitModel,
)


class RouteModel(VersionedModel):
    category: Optional[str]
    category_name: Optional[str]
    role_name: Optional[List]
    role_id_list: Optional[List]
    path: str
    entry_code: Optional[str]
    access_strategy: str
    access_strategy_name: Optional[str]

    permit_list: Optional[List[RoutePermitEditModel]] = []

    def to_route_permit_model(self, route_id: str) -> List[RoutePermitModel]:
        route_permit_models = []
        for permitted_resource_id in self.role_id_list:
            category_model = RoutePermitModel(
                route_id=route_id,
                permitted_resource_category=EnumRoutePermitResourceCategory.ROLE.name,
                permitted_resource_id=permitted_resource_id,
            )
            route_permit_models.append(category_model)
        return route_permit_models


class EnumRouteCategory(Enum):
    """
    路由类型
    """

    BACKEND = "后端"
    FRONTEND = "前端"


class EnumRouteAccessStrategy(Enum):
    """
    路由访问策略
    """

    IGNORE = "忽略"
    AUTHORIZED = "身份验证"
    CONTROLLED = "受控"
