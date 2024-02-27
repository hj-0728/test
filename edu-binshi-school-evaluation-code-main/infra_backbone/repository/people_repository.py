from typing import List, Optional

from infra_basic.basic_repository import BasicRepository, OrderCondition, PageInitParams
from infra_basic.pagination_carrier import PaginationCarrier
from infra_basic.transaction import Transaction

from infra_backbone.data.params.people_page_query_params import PeoplePageQueryParams
from infra_backbone.entity.people import PeopleEntity
from infra_backbone.model.contact_info_model import EnumContactInfoCategory
from infra_backbone.model.identity_number_model import EnumIdentityNumberOwnerCategory
from infra_backbone.model.params.people_params import PeopleQueryParams
from infra_backbone.model.people_model import PeopleModel
from infra_backbone.model.resource_contact_info_model import EnumContactInfoResourceCategory
from infra_backbone.model.role_model import EnumRoleCode
from infra_backbone.model.view.people_info_vm import PeopleInfoVm
from infra_backbone.model.view.people_page_vm import PeoplePageVm


class PeopleRepository(BasicRepository):
    def insert_people(self, data: PeopleModel, transaction: Transaction) -> str:
        """
        插入人员
        :param data:
        :param transaction:
        :return:
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=PeopleEntity, entity_model=data, transaction=transaction
        )

    def delete_people_by_id(self, people_id: str, transaction: Transaction):
        """
        根据人员id删除人员
        :param people_id: 人员id
        :param transaction: 交易
        :return:
        """

        self._delete_versioned_entity_by_id(
            entity_cls=PeopleEntity, entity_id=people_id, transaction=transaction
        )

    def update_people(
        self,
        people_id: str,
        version: int,
        people: PeopleModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """
        更新人员
        :param people_id:
        :param version:
        :param people:
        :param transaction:
        :param limited_col_list:
        :return:
        """

        self._update_versioned_entity_by_dict(
            entity_cls=PeopleEntity,
            entity_id=people_id,
            version=version,
            update_data=people.dict(),
            transaction=transaction,
            limited_col_list=limited_col_list,
        )

    def get_people_page(
        self,
        params: PeoplePageQueryParams,
    ) -> PaginationCarrier[PeoplePageVm]:
        """
        获取人员列表 分页
        :param params:
        :return:
        """
        sql = """
        WITH children_list AS (
        SELECT st2.*
        FROM sv_dimension_dept_tree st1 
        INNER JOIN sv_dimension_dept_tree st2 ON st1.id = ANY(st2.path_list)
        where true
        """
        if params.dimension_dept_tree_id:
            sql += " and st1.dimension_dept_tree_id = :dimension_dept_tree_id "
        sql += """
        AND st1.organization_id = :organization_id
        AND st2.organization_id = :organization_id
        AND st2.dimension_id = :dimension_id
        ),dept_people as (
        SELECT DISTINCT sp.id,sp.name,sp.gender,se.id as establishment_id,
        sd.name as dept_name,cl.display_name,st.id as dimension_dept_tree_id
        FROM st_people sp
        INNER JOIN st_establishment_assign ea on ea.people_id=sp.id and ea.finish_at>now()
        INNER JOIN st_establishment se ON se.id = ea.establishment_id and se.finish_at>now()
        INNER JOIN st_dimension_dept_tree st ON st.id = se.dimension_dept_tree_id
        INNER JOIN st_capacity sc ON sc.id = se.capacity_id AND sc.code = 'MEMBER'
        INNER JOIN st_dept sd ON sd.id=st.dept_id
        INNER JOIN children_list cl ON cl.dimension_dept_tree_id = st.id
        )
        ,data_list AS (
        SELECT id,name,gender,
        array_agg(json_build_object('establishment_id',establishment_id,'name',dept_name)) AS dept_list,
        array_agg(dimension_dept_tree_id) AS dimension_dept_tree_id_list,
        string_agg(display_name, '、') AS dept
        FROM dept_people
        GROUP BY id,name,gender
        )
        SELECT *
        FROM data_list WHERE TRUE
        """

        if params.gender_list:
            sql += """
            AND gender = ANY(:gender_list)
            """
        if params.not_show_children:
            sql += """
            AND :dimension_dept_tree_id =  ANY(dimension_dept_tree_id_list)
            """

        page_init_params = PageInitParams(
            sql=sql,
            filter_columns=["name"],
            order_columns=[
                OrderCondition(column_name="name", order="asc"),
            ],
            params={
                "gender_list": params.gender_list,
                "dimension_dept_tree_id": params.dimension_dept_tree_id,
                "organization_id": params.organization_id,
                "dimension_id": params.dimension_id,
            },
        )
        return self._paginate(
            result_type=PeoplePageVm,
            total_params=page_init_params,
            page_params=params,
        )

    def get_people_by_name(self, name: str) -> Optional[PeopleModel]:
        """
        根据名称获取人员信息
        :param name:
        :return:
        """

        sql = """select * from st_people where name = :name"""
        return self._fetch_first_to_model(model_cls=PeopleModel, sql=sql, params={"name": name})

    def get_people_by_remote_user_id(self, remote_user_id: str) -> List[PeopleModel]:
        """
        根据名称获取人员信息
        :param remote_user_id:
        :return:
        """

        sql = """select sp.* from st_people sp
        join st_context_people_user_map scpum on scpum.people_id = sp.id
        join st_dingtalk_user sdu on sdu.id = scpum.res_id and scpum.res_category = 'DINGTALK_USER'
        where sdu.remote_user_id = :remote_user_id
        union all
        select sp.* from st_people sp
        join st_context_people_user_map scpum on scpum.people_id = sp.id
        join st_dingtalk_k12_parent sdkp on sdkp.id = scpum.res_id and scpum.res_category = 'DINGTALK_K12_PARENT'
        where sdkp.remote_user_id = :remote_user_id
        """
        return self._fetch_all_to_model(
            model_cls=PeopleModel, sql=sql, params={"remote_user_id": remote_user_id}
        )

    def get_people_info_by_id(self, people_id: str) -> Optional[PeopleInfoVm]:
        """
        根据id获取人员信息
        :param people_id:
        :return:
        """

        sql = """
        SELECT sp.id,sp.name,sp.gender,sp.born_at,sp.is_verified,
        COALESCE(json_agg(sci.detail) FILTER (WHERE sci.detail IS NOT NULL), '[]') AS phone_list,
        (
        SELECT COALESCE(json_agg(json_build_object('category',sn.category,'number',sn.number)) 
        FILTER (WHERE sn.category IS NOT NULL), '[]') 
        FROM st_identity_number sn
        WHERE sn.owner_id = sp.id
        ) AS number_info
        FROM st_people sp
        LEFT JOIN st_resource_contact_info si ON si.resource_id=sp.id AND si.resource_category=:PEOPLE
        LEFT JOIN st_contact_info sci ON sci.id=si.contact_info_id AND sci.category=:PHONE
        WHERE sp.id=:people_id
        GROUP BY sp.id
        """
        return self._fetch_first_to_model(
            model_cls=PeopleInfoVm,
            sql=sql,
            params={
                "people_id": people_id,
                "PEOPLE": EnumContactInfoResourceCategory.PEOPLE.name,
                "PHONE": EnumContactInfoCategory.PHONE.name,
            },
        )

    def get_people_info_by_identity_number(
        self, identity_category: str, identity_number: str
    ) -> Optional[PeopleInfoVm]:
        """
        根据证件号获取人员信息
        """
        sql = """
        select sp.* from st_people sp
        join st_identity_number sin
        on sp.id = sin.owner_id and sin.owner_category = 'PEOPLE'
        where sin.number = :identity_number and sin.category = :identity_category
        """
        return self._fetch_first_to_model(
            model_cls=PeopleInfoVm,
            sql=sql,
            params={
                "identity_category": identity_category,
                "identity_number": identity_number,
                "people": EnumIdentityNumberOwnerCategory.PEOPLE.name,
            },
        )

    def get_people_info_list_by_people_id_list(
        self,
        allow_dept_id_list: List[str],
        people_id_list: List[str],
        contact_info_category_list: List[str],
    ) -> List[PeoplePageVm]:
        """
        根据人员id列表获取人员信息列表
        :param allow_dept_id_list:
        :param people_id_list:
        :param contact_info_category_list:
        :return:
        """
        sql = """
        WITH people_list AS (
        SELECT sp.id,sp.name,sp.gender,sd.name || '-' || spn.name AS position_name,spn.code AS position_code,
        sd.id AS dept_id,sd.name AS dept_name,st.seq + se.seq AS seq
        FROM st_people sp
        INNER JOIN st_establishment se ON se.people_id = sp.id
        INNER JOIN st_dimension_dept_tree st ON st.id=se.dimension_dept_tree_id
        INNER JOIN st_dept sd ON sd.id=st.dept_id
        INNER JOIN st_organization so ON so.id=sd.organization_id
        INNER JOIN st_dimension sdn ON sdn.id=st.dimension_id
        INNER JOIN st_position spn ON spn.id=se.position_id
        WHERE sp.id=ANY(:people_id_list) AND sd.id=ANY(:allow_dept_id_list) ORDER BY sp.id,st.seq,se.seq
        ),people_list_agg as (
        SELECT id, name, gender,array_agg(seq) AS seq,
        json_agg(json_build_object('name',position_name,'code',position_code)) AS position_list,
        json_agg(json_build_object('id',dept_id,'name',dept_name)) AS dept_list
        FROM people_list GROUP BY id,name,gender
        ),contact_info_list AS (
        SELECT pa.id,sci.category,sci.detail FROM people_list_agg pa
        INNER JOIN st_resource_contact_info si ON si.resource_id=pa.id AND si.resource_category=:PEOPLE 
        INNER JOIN st_contact_info sci ON sci.id=si.contact_info_id AND sci.category=ANY(:contact_info_category_list) 
        ORDER BY pa.id,sci.category DESC
        ),contact_info_agg AS (
        SELECT cl.id,json_agg(json_build_object('category',cl.category,'detail',cl.detail)) AS contact_info_list
        FROM contact_info_list cl GROUP BY cl.id
        )
        SELECT pa.*,ca.contact_info_list FROM people_list_agg pa
        LEFT JOIN contact_info_agg ca ON ca.id = pa.id ORDER BY pa.seq,pa.name DESC
        """

        return self._fetch_all_to_model(
            model_cls=PeoplePageVm,
            sql=sql,
            params={
                "PEOPLE": EnumContactInfoResourceCategory.PEOPLE.name,
                "allow_dept_id_list": allow_dept_id_list,
                "people_id_list": people_id_list,
                "contact_info_category_list": contact_info_category_list,
            },
        )

    def get_people_self_info_by_id(self, people_id: str) -> Optional[PeopleModel]:
        """
        获取人员本身的信息
        :param people_id:
        :return:
        """
        sql = """select * from st_people where id = :people_id"""
        return self._fetch_first_to_model(
            model_cls=PeopleModel, sql=sql, params={"people_id": people_id}
        )

    def get_people_list(self, query_params: PeopleQueryParams) -> PaginationCarrier[PeopleModel]:
        """
        获取人员列表
        """
        sql = """
        select * from st_people sp
        """
        if query_params.gender_list:
            sql += """
            WHERE sp.gender = ANY(:gender_list)
            """
        page_init_params = PageInitParams(
            sql=sql,
            filter_columns=[
                "name",
            ],
            order_columns=[
                OrderCondition(column_name="name", order="asc"),
            ],
            params={
                "gender_list": query_params.gender_list,
            },
        )
        return self._paginate(
            result_type=PeopleModel,
            total_params=page_init_params,
            page_params=query_params,
        )

    def get_people_page_for_dept_people_select(
        self, params: PeoplePageQueryParams
    ) -> PaginationCarrier[PeopleModel]:
        """
        获取人员列表
        """
        sql = """
        WITH people_list AS (
        SELECT sp.*
        FROM st_establishment se
        INNER JOIN st_dimension_dept_tree st ON st.id = se.dimension_dept_tree_id
        INNER JOIN st_dimension sd ON sd.id = st.dimension_id
        INNER JOIN st_people sp ON sp.id = se.people_id
        WHERE se.dimension_dept_tree_id = :dimension_dept_tree_id
        AND sd.organization_id = :organization_id
        AND se.position_id = :position_id
        ), data_list AS(
        SELECT * FROM st_people sp
        EXCEPT
        SELECT * FROM people_list
        )
        SELECT * FROM data_list
        """
        if params.gender_list:
            sql += """
            WHERE gender = ANY(:gender_list)
            """
        page_init_params = PageInitParams(
            sql=sql,
            filter_columns=[
                "name",
            ],
            order_columns=[
                OrderCondition(column_name="name", order="asc"),
            ],
            params={
                "gender_list": params.gender_list,
                "dimension_dept_tree_id": params.dimension_dept_tree_id,
                "organization_id": params.organization_id,
                "position_id": params.position_id,
            },
        )
        return self._paginate(
            result_type=PeopleModel,
            total_params=page_init_params,
            page_params=params,
        )

    def get_people_by_user_id_and_role_code(
        self, user_id: str, role_code: str
    ) -> Optional[PeopleModel]:
        """
        根据用户id跟当前role_code获取people信息
        :param user_id:
        :param role_code:
        :return:
        """
        if role_code == EnumRoleCode.STUDENT.name:
            sql = """
            select sp.* from st_people sp
            inner join st_people_user pu on sp.id = pu.people_id
            INNER JOIN st_establishment_assign ea on ea.people_id = sp.id
            INNER JOIN st_establishment se on se.id = ea.establishment_id
            INNER JOIN st_capacity sc on se.capacity_id = sc.id 
            where pu.user_id = :user_id and sp.is_available is true 
            and sc.code = 'STUDENT'
            GROUP BY sp.id
            """
        else:
            sql = """
            select sp.* from st_people sp
            inner join st_people_user pu on sp.id = pu.people_id
            INNER JOIN st_establishment_assign ea on ea.people_id = sp.id
            INNER JOIN st_establishment se on se.id = ea.establishment_id
            INNER JOIN st_capacity sc on se.capacity_id = sc.id 
            where pu.user_id = :user_id and sp.is_available is true 
            and sc.code <> 'STUDENT'
            GROUP BY sp.id
            """

        return self._fetch_first_to_model(
            sql=sql,
            model_cls=PeopleModel,
            params={"user_id": user_id},
        )
