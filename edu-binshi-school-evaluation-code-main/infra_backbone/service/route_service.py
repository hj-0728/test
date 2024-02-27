from typing import Dict, List, Optional, Set

from infra_basic.errors.input import DataNotFoundError
from infra_basic.pagination_carrier import PaginationCarrier
from infra_basic.transaction import Transaction
from infra_utility.algorithm.tree import list_to_tree
from infra_utility.enum_helper import get_enum_value_by_name
from loguru import logger

from infra_backbone.model.ability_permission_assign_model import (
    AbilityPermissionAssignTreeViewModel,
)
from infra_backbone.model.params.route_query_params import RouteQueryParams
from infra_backbone.model.route_model import EnumRouteAccessStrategy, EnumRouteCategory, RouteModel
from infra_backbone.model.route_permit_model import (
    EnumRoutePermitResourceCategory,
    RoutePermitModel,
)
from infra_backbone.repository.route_repository import RouteRepository


class RouteService:
    def __init__(
        self,
        route_repository: RouteRepository,
    ):
        self.__route_repository = route_repository

    def refresh_route(
        self,
        ignore_path: List[str],
        flask_app_route_set: Set[str],
        remove_unused: bool,
        transaction: Transaction,
    ):
        """

        :param ignore_path:
        :param flask_app_route_set:
        :param remove_unused:
        :param transaction:
        :return:
        """

        db_route_list = self.__route_repository.fetch_route_list_by_category(
            category=EnumRouteCategory.BACKEND.name
        )
        db_route_set = {r.path for r in db_route_list}

        new_route_set = flask_app_route_set - db_route_set
        self.add_new_route(
            route_list=new_route_set, ignore_path=ignore_path, transaction=transaction
        )
        db_route_dict: Dict[str, str] = {x.path: x.id for x in db_route_list}
        if remove_unused:
            need_delete_route_set = db_route_set - flask_app_route_set
            for route in need_delete_route_set:
                db_route_id = db_route_dict.get(route)
                if db_route_id:
                    self.__route_repository.delete_route(
                        route_id=db_route_id, transaction=transaction
                    )

    def add_new_route(self, route_list: Set[str], ignore_path: List[str], transaction: Transaction):
        """

        :param route_list:
        :param ignore_path:
        :param transaction:
        :return:
        """

        for new_route in route_list:
            if new_route in ignore_path or new_route.startswith("/test"):
                access_strategy = EnumRouteAccessStrategy.IGNORE.name
            else:
                access_strategy = EnumRouteAccessStrategy.AUTHORIZED.name

            route = RouteModel(
                path=new_route,
                category=EnumRouteCategory.BACKEND.name,
                access_strategy=access_strategy,
            )
            try:
                self.__route_repository.insert_route(data=route, transaction=transaction)
            except Exception as error:
                logger.error(str(error))

    def get_route_with_permit(self) -> Dict[str, Optional[List[RouteModel]]]:
        """

        :return:
        """

        route_list = self.__route_repository.get_route_with_permit()
        return {x.path: x for x in route_list}

    def add_route_permit(
        self,
        path: str,
        route_permit_list: List[RoutePermitModel],
        transaction: Transaction,
    ):
        """

        :param path:
        :param route_permit_list:
        :param transaction:
        :return:
        """
        route_info = self.__route_repository.get_route_by_path(path=path)
        if not route_info:
            raise DataNotFoundError("未获取到路由信息")

        if route_info.access_strategy != EnumRouteAccessStrategy.CONTROLLED.name:
            route_info.access_strategy = EnumRouteAccessStrategy.CONTROLLED.name
            self.__route_repository.update_route(
                data=route_info,
                transaction=transaction,
                limited_col_list=["access_strategy"],
            )

        for route_permit in route_permit_list:
            route_permit.route_id = route_info.id
            self.__route_repository.insert_route_permit(
                data=route_permit,
                transaction=transaction,
            )

    def get_path_list(self, query_params: RouteQueryParams) -> PaginationCarrier[RouteModel]:
        """
        获取路径列表信息
        """
        result = self.__route_repository.get_path_list(
            query_params=query_params,
        )
        for data in result.data:
            data.category_name = get_enum_value_by_name(
                enum_class=EnumRouteCategory,
                enum_name=data.category,
            )
            data.access_strategy_name = get_enum_value_by_name(
                enum_class=EnumRouteAccessStrategy,
                enum_name=data.access_strategy,
            )
        return result

    # def edit_path(self, data: RouteModel, transaction: Transaction):
    #     return self.__route_repository.update_path(
    #         data=RouteModel(
    #             id=data.id,
    #             version=data.version,
    #             path=data.path,
    #             access_strategy=data.access_strategy,
    #         ),
    #         transaction=transaction,
    #         limited_col_list=["access_strategy", "entry_code"],
    #     )
    def edit_path(self, data: RouteModel, transaction: Transaction):
        self.__route_repository.update_path(
            data=data,
            transaction=transaction,
            limited_col_list=["access_strategy", "entry_code"],
        )

        self.update_route_permit(
            data,
            permitted_resource_category=EnumRoutePermitResourceCategory.ROLE.name,
            transaction=transaction,
        )

        self.update_route_permit(
            data,
            permitted_resource_category=EnumRoutePermitResourceCategory.ABILITY_PERMISSION.name,
            transaction=transaction,
        )

    def update_route_permit(
        self, data: RouteModel, permitted_resource_category: str, transaction: Transaction
    ):
        original_ability_permission_assign_list = (
            self.__route_repository.get_route_ability_permission_assign_by_params(
                permitted_resource_category=permitted_resource_category,
                route_id=data.id,
            )
        )

        for original_ability_permission_assign in original_ability_permission_assign_list:
            self.__route_repository.delete_route_permit(
                route_permit_id=original_ability_permission_assign.id, transaction=transaction
            )

        if permitted_resource_category == EnumRoutePermitResourceCategory.ROLE.name:
            route_permit_list = data.to_route_permit_model(data.id)
        else:
            route_permit_list = data.permit_list[0].to_route_permit_model(data.id)

        for route_permit in route_permit_list:
            self.__route_repository.insert_route_permit(data=route_permit, transaction=transaction)

    def get_route_ability_permission_assign_tree(self, route_id: str):
        tree_list = self.__route_repository.get_route_ability_permission_assign_tree(
            route_id=route_id
        )

        tree = list_to_tree(
            original_list=tree_list,
            tree_node_type=AbilityPermissionAssignTreeViewModel,
            seq_attr="tree_seq",
        )
        return tree
