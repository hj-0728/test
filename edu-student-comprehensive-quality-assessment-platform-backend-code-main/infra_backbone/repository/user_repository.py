from typing import List, Optional

from infra_basic.basic_repository import BasicRepository, OrderCondition, PageInitParams
from infra_basic.pagination_carrier import PaginationCarrier
from infra_basic.transaction import Transaction

from infra_backbone.entity.oranization_user_map import OrganizationUserMapEntity
from infra_backbone.entity.user import UserEntity
from infra_backbone.model.ability_permission_assign_model import AbilityPermissionAssignModel
from infra_backbone.model.organization_user_map_model import OrganizationUserMapModel
from infra_backbone.model.params.user_params import UserQueryParams
from infra_backbone.model.user_model import UserModel
from infra_backbone.model.user_role_model import UserRoleModel
from infra_backbone.model.view.user_profile_vm import UserProfileViewModel


class UserRepository(BasicRepository):
    def get_user_by_name(self, name: str) -> Optional[UserModel]:
        """

        :param name:
        :return:
        """
        sql = """
        select * from st_user where name=:name
        """
        return self._fetch_first_to_model(sql=sql, model_cls=UserModel, params={"name": name})

    def get_user_by_id(self, user_id: str) -> Optional[UserModel]:
        """
        根据用户id获取用户信息
        :param user_id:
        :return:
        """
        sql = """
        select * from st_user where id=:user_id
        """
        return self._fetch_first_to_model(sql=sql, model_cls=UserModel, params={"user_id": user_id})

    def insert_user(self, data: UserModel, transaction: Transaction) -> str:
        """
        插入用户
        :param data:
        :param transaction:
        :return:
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=UserEntity,
            entity_model=data,
            transaction=transaction,
        )

    def update_user(
        self,
        data: UserModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """

        :param data:
        :param transaction:
        :param limited_col_list:
        :return:
        """

        return self._update_versioned_entity_by_model(
            entity_cls=UserEntity,
            update_model=data,
            limited_col_list=limited_col_list,
            transaction=transaction,
        )

    def get_user_role_by_user_name_and_role_code(
        self, user_name: str, role_code: str
    ) -> Optional[UserRoleModel]:
        """
        根据用户名称和角色编码获取用户角色
        :param user_name:
        :param role_code:
        :return:
        """
        sql = """
        SELECT sur.* FROM st_role sr 
        INNER JOIN st_user_role sur on sr.id = sur.role_id 
        INNER JOIN st_user su on sur.user_id = su.id
        WHERE su.name = :user_name and sr.code = :role_code
        """
        return self._fetch_first_to_model(
            sql=sql,
            model_cls=UserRoleModel,
            params={"user_name": user_name, "role_code": role_code},
        )

    def insert_organization_user(
        self, data: OrganizationUserMapModel, transaction: Transaction
    ) -> str:
        """
        插入组织用户
        :param data:
        :param transaction:
        :return:
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=OrganizationUserMapEntity,
            entity_model=data,
            transaction=transaction,
        )

    def get_user_list(
        self,
        params: UserQueryParams,
    ) -> PaginationCarrier[UserModel]:
        """
        获取用户列表
        """
        sql = """
        with exclude_user_ids as (
        select distinct sur.user_id from st_role sr
        inner join st_user_role sur on sur.role_id = sr.id
        where sr.code = any(array[:filter_out_role_code])
        ),
        user_role as (
        select sur.user_id, array_agg(sr.id) AS role_id_list, array_agg(sr.name 
        order by case when sr.code = 'SYSTEM_ADMIN' then 1 
        when sr.code = 'ADMIN' then 2 
        when sr.code = 'TEACHER' then 3 
        else 4 end
        ) as role_name_list,
        array_agg(sr.code) as role_code_list
        from st_user_role sur
        inner join st_role sr on sr.id = sur.role_id
        where not exists (select * from exclude_user_ids ui where ui.user_id = sur.user_id)
        group by sur.user_id
        )
        select su.*, ur.role_id_list,role_name_list,p.name as people_name,
        pu.people_id,
        array_to_string(role_name_list, ' ') as role_name_string
        from st_user su
        inner join user_role ur on ur.user_id = su.id
        left join st_people_user pu on pu.user_id=su.id
        left join st_people p on p.id=pu.people_id
        """

        if params.is_activated:
            sql += """where is_activated = :is_activated"""

        page_init_params = PageInitParams(
            sql=sql,
            filter_columns=["name", "role_name_string", "people_name"],
            order_columns=[
                OrderCondition(column_name="name"),
            ],
            params={
                "is_activated": params.is_activated,
                "filter_out_role_code": params.filter_out_role_code,
            },
        )
        return self._paginate(
            result_type=UserModel,
            total_params=page_init_params,
            page_params=params,
        )

    def get_same_user_name(self, name: str, user_id: str) -> Optional[UserModel]:
        """
        获取同名用户
        """
        sql = """
         select * from st_user where id!=:user_id and  name=:name
         """
        return self._fetch_first_to_model(
            sql=sql, model_cls=UserModel, params={"user_id": user_id, "name": name}
        )

    def get_user_ability_permission(
        self, user_id: str, role_id: str
    ) -> List[AbilityPermissionAssignModel]:
        """

        :param user_id:
        :param role_id:
        :return:
        """

        sql = """
        select * from st_ability_permission_assign 
        where assign_resource_category='ROLE' and assign_resource_id=:role_id
        union
        select * from st_ability_permission_assign 
        where assign_resource_category='USER' and assign_resource_id=:user_id
        """

        return self._fetch_all_to_model(
            sql=sql,
            model_cls=AbilityPermissionAssignModel,
            params={"role_id": role_id, "user_id": user_id},
        )

    def get_user_profile(
        self,
        user_id: str,
        role_id: str,
    ) -> Optional[UserProfileViewModel]:
        """
        获取用户信息
        :param user_id:
        :param role_id:
        :return:
        """
        sql = """
        select sr.id as role_id, sr.code as role_code, su.id as user_id
        from st_user su
        inner join st_user_role sur on su.id = sur.user_id
        inner join st_role sr on sr.id = sur.role_id
        where su.id = :user_id
        and sr.id = :role_id
       """
        return self._fetch_first_to_model(
            model_cls=UserProfileViewModel,
            sql=sql,
            params={
                "user_id": user_id,
                "role_id": role_id,
            },
        )

    def get_special_role_user_list(self, exist_role_code_list: List[str], need_add_role_code: str):
        """
        获取拥有指定角色的用户,且不存在需要添加的角色的用户
        给在系统的校长与行政增加教师的角色
        """
        sql = """
         with result as (select distinct su.*,array_agg(sr.code) as code_list  from st_user su 
        inner join st_user_role ur on ur.user_id = su.id 
        inner join st_role sr on sr.id = ur.role_id
        GROUP BY su.id)
        select * from result
        where code_list::text[] && array[:exist_role_code_list] 
        and not(:need_add_role_code = any(code_list::text[]))
        """
        return self._fetch_all_to_model(
            model_cls=UserModel,
            sql=sql,
            params={
                "exist_role_code_list": exist_role_code_list,
                "need_add_role_code": need_add_role_code,
            },
        )

    def get_user_list_by_people_id_list(self, people_id_list: List[str]) -> List[UserModel]:
        """
        通过人员id列表获取用户列表
        :param people_id_list:
        :return:
        """

        sql = """
        select u.*,pu.people_id
        from st_people_user pu 
        inner join st_user u on pu.user_id=u.id
        where people_id = any(array[:people_id_list])
        """
        return self._fetch_all_to_model(
            model_cls=UserModel, sql=sql, params={"people_id_list": people_id_list}
        )

    def fetch_user_list_by_role_code(self, role_code: str) -> List[UserModel]:
        """
        通过角色编码获取用户列表
        """
        sql = """
        select distinct su.* from st_user su
        inner join st_user_role sur on sur.user_id = su.id
        inner join st_role sr on sr.id = sur.role_id
        where sr.code = :role_code
        and su.is_activated is true
        """
        return self._fetch_all_to_model(
            model_cls=UserModel, sql=sql, params={"role_code": role_code}
        )

    def fetch_need_disable_user(self) -> List[UserModel]:
        """
        获取需要禁用的用户
        """
        sql = """
        select su.* from st_people sp
        inner join st_people_user spu on spu.people_id = sp.id
        inner join st_user su on su.id = spu.user_id
        where sp.is_activated is false
        and su.is_activated is true
        """
        return self._fetch_all_to_model(model_cls=UserModel, sql=sql)
