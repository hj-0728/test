from typing import List, Optional

from infra_basic.basic_repository import BasicRepository, OrderCondition, PageInitParams
from infra_basic.pagination_carrier import PaginationCarrier
from infra_basic.transaction import Transaction

from infra_backbone.entity.organization import OrganizationEntity
from infra_backbone.entity.organization_address import OrganizationAddressEntity
from infra_backbone.model.area_model import AreaModel
from infra_backbone.model.organization_address_model import OrganizationAddressModel
from infra_backbone.model.organization_model import OrganizationModel
from infra_backbone.model.params.organization_params import OrganizationQueryParams


class OrganizationRepository(BasicRepository):
    def insert_organization(self, data: OrganizationModel, transaction: Transaction) -> str:
        """
        插入组织
        :param data:
        :param transaction:
        :return:
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=OrganizationEntity,
            entity_model=data,
            transaction=transaction,
        )

    def get_organization_by_code(self, code: str) -> Optional[OrganizationModel]:
        """
        根据code获取组织
        :param code:
        :return:
        """

        sql = """select * from st_organization where code = :code"""
        return self._fetch_first_to_model(
            model_cls=OrganizationModel, sql=sql, params={"code": code}
        )

    def insert_organization_address(self, data: OrganizationAddressModel, transaction: Transaction):
        """
        插入组织地址
        :param data:
        :param transaction:
        :return:
        """
        self._insert_versioned_entity_by_model(
            entity_cls=OrganizationAddressEntity,
            entity_model=data,
            transaction=transaction,
        )

    def fetch_organization_address_belong_area(
        self, organization_id: str, seq: int = 1
    ) -> Optional[AreaModel]:
        """
        获取组织地址所属地域
        :param organization_id:
        :param seq: 默认获取组织排在第一位的地址所属区域id
        :return: area id
        """
        sql = """select sa2.* from st_organization_address soa
        inner join st_address sa on sa.id = soa.address_id
        inner join st_area sa2 on sa2.id = sa.area_id
        where soa.organization_id = :organization_id and soa.seq = :seq
        """
        return self._fetch_first_to_model(
            model_cls=AreaModel,
            sql=sql,
            params={"organization_id": organization_id, "seq": seq},
        )

    def fetch_organization_by_name(self, name: str) -> Optional[OrganizationModel]:
        """
        根据名称获取组织
        :param name:
        :return:
        """
        sql = """select * from st_organization where name = :name"""
        return self._fetch_first_to_model(
            model_cls=OrganizationModel, sql=sql, params={"name": name}
        )

    def fetch_organization_by_code(self, code: Optional[str]) -> Optional[OrganizationModel]:
        """
        根据编码获取组织
        :param code:
        :return:
        """
        sql = """select * from st_organization where code = :code"""
        return self._fetch_first_to_model(
            model_cls=OrganizationModel, sql=sql, params={"code": code}
        )

    def get_organization_list_by_category(
        self,
        category: str,
    ) -> List[OrganizationModel]:
        """
        根据类型获取所有组织
        :param category:
        :return:
        """

        sql = """select * from st_organization
        where category = :category order by name"""
        return self._fetch_all_to_model(
            model_cls=OrganizationModel,
            sql=sql,
            params={"category": category},
        )

    def get_organization_by_id(self, organization_id: str) -> Optional[OrganizationModel]:
        """
        根据organization_id获取组织
        :param organization_id:
        :return:
        """

        sql = """select * from st_organization where id = :organization_id"""
        return self._fetch_first_to_model(
            model_cls=OrganizationModel,
            sql=sql,
            params={"organization_id": organization_id},
        )

    def get_organization_list(
        self,
        query_params: OrganizationQueryParams,
    ) -> PaginationCarrier[OrganizationModel]:
        """
        获取组织列表
        """
        sql = """
        select so.id,so.name,so.code,so.category,sdd.name as category_name,so.is_activated,so.version 
        from st_organization so
        INNER JOIN st_dict_data sdd on sdd.code = so.category
        where TRUE
        """
        if query_params.category:
            sql += " and category = any(:category)"

        page_init_params = PageInitParams(
            sql=sql,
            filter_columns=["name", "code"],
            order_columns=[
                OrderCondition(column_name="name", order="asc"),
            ],
            params={
                "category": query_params.category,
            },
        )
        return self._paginate(
            result_type=OrganizationModel,
            total_params=page_init_params,
            page_params=query_params,
        )

    def get_same_organization_name(
        self,
        name: str,
        organization_id: str,
    ):
        """
        获取同名组织
        """
        sql = """
                select * from st_organization where id!=:organization_id and  name=:name
                """
        return self._fetch_first_to_model(
            sql=sql,
            model_cls=OrganizationModel,
            params={"organization_id": organization_id, "name": name},
        )

    def update_organization(
        self,
        data: OrganizationModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """
        更新组织
        """
        return self._update_versioned_entity_by_model(
            entity_cls=OrganizationEntity,
            update_model=data,
            transaction=transaction,
            limited_col_list=limited_col_list,
        )
