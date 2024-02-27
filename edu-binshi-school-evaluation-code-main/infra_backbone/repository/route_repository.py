from typing import List, Optional

from infra_basic.basic_repository import (
    BasicRepository,
    OrderCondition,
    PageInitParams,
    PaginationCarrier,
)
from infra_basic.transaction import Transaction

from infra_backbone.entity.route import RouteEntity
from infra_backbone.entity.route_permit import RoutePermitEntity
from infra_backbone.model.ability_permission_assign_model import (
    AbilityPermissionAssignTreeViewModel,
)
from infra_backbone.model.params.route_query_params import RouteQueryParams
from infra_backbone.model.route_model import RouteModel
from infra_backbone.model.route_permit_model import (
    EnumRoutePermitResourceCategory,
    RoutePermitModel,
)
from infra_backbone.model.view.route_vm import RouteViewModel


class RouteRepository(BasicRepository):
    def insert_route(self, data: RouteModel, transaction: Transaction) -> str:
        """
        插入路由
        :param data:
        :param transaction:
        :return:
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=RouteEntity,
            entity_model=data,
            transaction=transaction,
        )

    def insert_route_permit(self, data: RoutePermitModel, transaction: Transaction) -> str:
        """
        插入路由配置
        :param data:
        :param transaction:
        :return:
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=RoutePermitEntity,
            entity_model=data,
            transaction=transaction,
        )

    def update_route(
        self,
        data: RouteModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ) -> int:
        """
        插入路由
        :param data:
        :param transaction:
        :param limited_col_list:
        :return:
        """

        return self._update_versioned_entity_by_model(
            entity_cls=RouteEntity,
            update_model=data,
            transaction=transaction,
            limited_col_list=limited_col_list,
        )

    def delete_route(
        self,
        route_id: str,
        transaction: Transaction,
    ):
        """

        :param route_id:
        :param transaction:
        :return:
        """

        self._delete_versioned_entity_by_id(
            entity_cls=RouteEntity,
            entity_id=route_id,
            transaction=transaction,
        )

    def fetch_route_list_by_category(self, category: str) -> List[RouteModel]:
        """

        :param category:
        :return:
        """

        sql = """
        select * from st_route where category=:category
        """

        return self._fetch_all_to_model(
            model_cls=RouteModel, sql=sql, params={"category": category}
        )

    def get_route_with_permit(self) -> List[RouteModel]:
        """

        :return:
        """
        sql = """
        with res as (
        select sr.id,
        json_build_object('permitted_resource_category', 
        permitted_resource_category, 'permitted_resource_ids', 
        array_agg(srp.permitted_resource_id)) as permit
        from st_route sr
        inner join st_route_permit srp
        on sr.id = srp.route_id
        group by sr.id,permitted_resource_category
        )
        select path, category,access_strategy,case when count(s.id) > 0 then 
        array_to_json(array_agg(permit)) else null end as permit_list
        from st_route r left join res s on r.id=s.id
        group by path, category,access_strategy
        """

        return self._fetch_all_to_model(model_cls=RouteModel, sql=sql)

    def get_route_by_path(self, path: str) -> Optional[RouteModel]:
        """

        :param path:
        :return:
        """

        sql = """
        select * from st_route where path=:path
        """
        return self._fetch_first_to_model(model_cls=RouteModel, sql=sql, params={"path": path})

    def fetch_route_list_by_category_and_prefix(
        self, prefix: str, category: str
    ) -> List[RouteModel]:
        """

        :param prefix:
        :param category:
        :return:
        """

        sql = """
        select * from st_route where category=:category and path ~ :prefix
        """

        return self._fetch_all_to_model(
            model_cls=RouteModel,
            sql=sql,
            params={"category": category, "prefix": prefix},
        )

    def get_path_list(self, query_params: RouteQueryParams) -> PaginationCarrier[RouteModel]:
        """
        获取路径列表
        """
        sql = """
        WITH role_data as (
        SELECT array_agg(DISTINCT sr.name) FILTER (WHERE sr.name IS NOT NULL) AS role_name_list, st_route.id 
        FROM st_route
        LEFT JOIN st_route_permit srp ON srp.route_id = st_route.id 
        LEFT JOIN st_role sr ON srp.permitted_resource_id = sr.id 
        AND srp.permitted_resource_category = :ROLE
        GROUP BY st_route.id
        ),
        ability_permission_data as (
        SELECT array_agg(DISTINCT sr.name) FILTER (WHERE sr.name IS NOT NULL) AS ability_permission_list, st_route.id 
        FROM st_route
        LEFT JOIN st_route_permit srp ON srp.route_id = st_route.id 
        LEFT JOIN st_ability_permission sr ON srp.permitted_resource_id = sr.id 
        AND srp.permitted_resource_category = :ABILITY_PERMISSION
        GROUP BY st_route.id
        )
        SELECT sr.*,rd.role_name_list,apd.ability_permission_list FROM st_route sr
        LEFT JOIN role_data rd on rd.id = sr.id
        LEFT JOIN ability_permission_data apd on apd.id = sr.id
        """
        if query_params.category:
            sql += " where sr.category = :category"
        if query_params.access_strategy:
            sql += " where sr.access_strategy = :access_strategy"
        page_init_params = PageInitParams(
            sql=sql,
            filter_columns=["path", "entry_code"],
            order_columns=[
                OrderCondition(column_name="path", order="asc"),
            ],
            params={
                "category": query_params.category,
                "access_strategy": query_params.access_strategy,
                "ABILITY_PERMISSION": EnumRoutePermitResourceCategory.ABILITY_PERMISSION.name,
                "ROLE": EnumRoutePermitResourceCategory.ROLE.name,
            },
        )
        return self._paginate(
            result_type=RouteViewModel,
            total_params=page_init_params,
            page_params=query_params,
        )

    def update_path(
        self,
        data: RouteModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        return self._update_versioned_entity_by_model(
            update_model=data,
            entity_cls=RouteEntity,
            transaction=transaction,
            limited_col_list=limited_col_list,
        )

    def get_route_ability_permission_assign_tree(
        self,
        route_id: str,
    ) -> List[AbilityPermissionAssignTreeViewModel]:
        """
        获取路由功能权限授权树
        """
        sql = """
        with result as(
            select sap.* ,
            case when srp.permitted_resource_id is not null then true else false end as granted
            from sv_ability_permission sap
            left join st_route_permit srp on sap.id = srp.permitted_resource_id and srp.route_id = :route_id
            AND srp.permitted_resource_category = :ABILITY_PERMISSION
            order by sort_info
        )
        select  * ,row_number() over () as tree_seq from result
        """
        return self._fetch_all_to_model(
            model_cls=AbilityPermissionAssignTreeViewModel,
            sql=sql,
            params={
                "route_id": route_id,
                "ABILITY_PERMISSION": EnumRoutePermitResourceCategory.ABILITY_PERMISSION.name,
            },
        )

    def get_route_ability_permission_assign_by_params(
        self,
        permitted_resource_category: str,
        route_id: str,
    ) -> List[RoutePermitModel]:
        """
        获取符合条件的路由功能权限授权
        """
        sql = """
        select * from st_route_permit
        where permitted_resource_category = :permitted_resource_category
        and route_id = :route_id
        """
        return self._fetch_all_to_model(
            model_cls=RoutePermitModel,
            sql=sql,
            params={
                "permitted_resource_category": permitted_resource_category,
                "route_id": route_id,
            },
        )

    def delete_route_permit(self, route_permit_id: str, transaction: Transaction):
        """

        :param route_permit_id:
        :param transaction:
        :return:
        """

        self._delete_versioned_entity_by_id(
            entity_cls=RoutePermitEntity, entity_id=route_permit_id, transaction=transaction
        )
