"""
permit许可信息配置
"""

from typing import List

from infra_basic.basic_model import BasePlusModel

from infra_backbone.model.route_permit_model import RoutePermitModel


class RoutePermitEditModel(BasePlusModel):
    """
    permit许可信息配置
    """

    permitted_resource_category: str
    permitted_resource_ids: List[str] = []

    def to_route_permit_model(self, route_id: str) -> List[RoutePermitModel]:
        route_permit_models = []
        for permitted_resource_id in self.permitted_resource_ids:
            category_model = RoutePermitModel(
                route_id=route_id,
                permitted_resource_category=self.permitted_resource_category,
                permitted_resource_id=permitted_resource_id,
            )
            route_permit_models.append(category_model)
        return route_permit_models
