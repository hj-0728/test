from typing import List, Optional

from infra_basic.basic_repository import (
    BasicRepository,
    OrderCondition,
    PageFilterParams,
    PageInitParams,
    PaginationCarrier,
)
from infra_basic.transaction import Transaction

from infra_backbone.entity.role import RoleEntity
from infra_backbone.model.role_model import EnumRoleCode, RoleModel


class RoleRepository(BasicRepository):
    def get_role_by_code(self, code: str) -> Optional[RoleModel]:
        """
        根据code获取角色
        :param code:
        :return:
        """
        sql = """
        select * from st_role where code=:code
        """
        return self._fetch_first_to_model(sql=sql, model_cls=RoleModel, params={"code": code})

    def insert_role(self, data: RoleModel, transaction: Transaction) -> str:
        """
        插入角色
        :param data:
        :param transaction:
        :return:
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=RoleEntity,
            entity_model=data,
            transaction=transaction,
        )

    def get_role_list_by_user_id(self, user_id: str) -> List[RoleModel]:
        """
        根据用户id获得角色列表
        :param user_id:
        :return:
        """
        sql = """
        SELECT sr.*, sur.id AS user_role_id FROM st_role sr 
        INNER JOIN st_user_role sur on sr.id = sur.role_id 
        INNER JOIN st_user su on sur.user_id = su.id
        WHERE su.id = :user_id
        and sr.is_activated is TRUE
        ORDER BY sr.code nulls last
        """
        return self._fetch_all_to_model(sql=sql, model_cls=RoleModel, params={"user_id": user_id})

    def get_role_by_id(self, role_id: str) -> Optional[RoleModel]:
        """
        根据role_id获取角色
        :param role_id:
        :return:
        """
        sql = """
        select * from st_role where id=:role_id
        """
        return self._fetch_first_to_model(sql=sql, model_cls=RoleModel, params={"role_id": role_id})

    def get_role_info(self):
        sql = """
        select * from st_role
        """
        return self._fetch_all_to_model(
            model_cls=RoleModel,
            sql=sql,
        )

    def get_role_page_list(
        self,
        search_text: Optional[str],
    ) -> List[RoleModel]:
        """
        获取角色列表
        # :param only_activated:
        # :param handler_id:
        :param search_text:
        :return:
        """
        sql = """
            SELECT * from st_role
            """
        params = {}
        if search_text:
            param_search_text = f"%{search_text.lower()}%"
            sql += """
                    where lower(name) like :param_search_text
                    """
            params["param_search_text"] = param_search_text
        return self._fetch_all_to_model(model_cls=RoleModel, sql=sql, params=params)

    def update_role_info(
        self,
        role: RoleModel,
        transaction: Transaction,
        col_list: Optional[List[str]] = None,
    ) -> str:
        """
        更新职责基本信息
        @param role:
        @param transaction:
        @param col_list:
        @return
        """
        return self._update_versioned_entity_by_model(
            update_model=role,
            entity_cls=RoleEntity,
            transaction=transaction,
            limited_col_list=col_list,
        )

    def get_role_by_name(
        self,
        name: str,
        filter_id: Optional[str] = None,
    ) -> Optional[RoleModel]:
        """
        :param name:
        :param filter_id:
        :return:
        """
        sql = """
        select * from st_role 
        where name=:name
        """
        if filter_id:
            sql += """ and id != :filter_id"""
        return self._fetch_first_to_model(
            model_cls=RoleModel,
            sql=sql,
            params={
                "name": name,
                "filter_id": filter_id,
            },
        )

    def get_role_by_code(
        self,
        code: str,
        filter_id: Optional[str] = None,
    ) -> Optional[RoleModel]:
        """
        :param code:
        :param filter_id:
        :return:
        """
        sql = """
        select * from st_role 
        where code=:code
        """
        if filter_id:
            sql += """ and id != :filter_id"""
        return self._fetch_first_to_model(
            model_cls=RoleModel,
            sql=sql,
            params={
                "code": code,
                "filter_id": filter_id,
            },
        )

    def get_all_role_list(self) -> List[RoleModel]:
        """
        获取所有启用的角色
        :return:
        """
        sql = """
        select * from st_role where is_activated is true order by name desc NULLS LAST
        """
        return self._fetch_all_to_model(sql=sql, model_cls=RoleModel)

    def get_role_list_page_info(
        self, query_params: PageFilterParams, current_role_code: str
    ) -> PaginationCarrier[RoleModel]:
        """
        获取角色列表页信息
        """
        sql = """
        select * from st_role
        where true
        """
        if current_role_code != EnumRoleCode.SYSTEM_ADMIN.name:
            sql += """
            and code != :system_admin_code
            """
        page_init_params = PageInitParams(
            sql=sql,
            order_columns=[OrderCondition(column_name="name")],
            filter_columns=[
                "name",
                "code",
            ],
            params={"system_admin_code": EnumRoleCode.SYSTEM_ADMIN.name},
        )
        return self._paginate(
            result_type=RoleModel,
            total_params=page_init_params,
            page_params=query_params,
        )

    def get_role_filter_list(self, role_code: str) -> List[RoleModel]:
        """
        获取角色 除管理员其他角色不能获取管理员
        """
        sql = """
        select sr.* from st_role sr 
        where is_activated is true 
        """
        if role_code != EnumRoleCode.SYSTEM_ADMIN.name:
            sql += """
            and code !=:system_admin
            """
        sql += """
        order by case when sr.code = 'HEADMASTER' then 1 
        when sr.code = 'ADMINISTRATION_STAFF' then 2 
        else 3 end
        """

        return self._fetch_all_to_model(
            sql=sql,
            model_cls=RoleModel,
            params={
                "role_code": role_code,
                "system_admin": EnumRoleCode.SYSTEM_ADMIN.name,
            },
        )
