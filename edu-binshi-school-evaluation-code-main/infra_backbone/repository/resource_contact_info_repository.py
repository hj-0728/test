from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_backbone.entity.resource_contact_info import ResourceContactInfoEntity
from infra_backbone.model.contact_info_model import ContactInfoModel
from infra_backbone.model.resource_contact_info_model import ResourceContactInfoModel


class ResourceContactInfoRepository(BasicRepository):
    def insert_resource_contact_info(
        self, data: ResourceContactInfoModel, transaction: Transaction
    ) -> str:
        """
        插入资源联系方式
        :param data:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=ResourceContactInfoEntity,
            entity_model=data,
            transaction=transaction,
        )

    def fetch_resource_contact_info(
        self, resource_id: str, resource_category: str
    ) -> Optional[ResourceContactInfoModel]:
        """
        获取资源的联系方式
        :param resource_id:
        :param resource_category:
        :return:
        """

        sql = """select sri.resource_id, sri.resource_category,
        array_agg(json_build_object('resource_contact_info_id', sri.id, 'category', 
        sci.category, 'detail', sci.detail)) as contact_info_list
        from st_resource_contact_info sri 
        inner join st_contact_info sci on sci.id = sri.contact_info_id
        where resource_id = :resource_id and resource_category  = :resource_category
        group by sri.resource_id, sri.resource_category"""
        return self._fetch_first_to_model(
            model_cls=ResourceContactInfoModel,
            sql=sql,
            params={"resource_id": resource_id, "resource_category": resource_category},
        )

    def delete_resource_contact_info(self, resource_contact_info_id: str, transaction: Transaction):
        """
        删除资源的联系方式
        :param resource_contact_info_id:
        :param transaction:
        :return:
        """
        self._delete_versioned_entity_by_id(
            entity_cls=ResourceContactInfoEntity,
            entity_id=resource_contact_info_id,
            transaction=transaction,
        )

    def get_exist_resource_contact_info(
        self,
        resource_category: str,
        resource_id: str,
        contact_info_id: str,
    ) -> List[ResourceContactInfoModel]:
        """
        获取资源联系方式
        :param resource_category:
        :param resource_id:
        :param contact_info_id:
        :return:
        """

        sql = """
        SELECT * FROM st_resource_contact_info srci
        WHERE srci.resource_category = :resource_category
        AND srci.resource_id = :resource_id
        AND srci.contact_info_id = :contact_info_id
        """

        return self._fetch_all_to_model(
            model_cls=ResourceContactInfoModel,
            sql=sql,
            params={
                "resource_category": resource_category,
                "resource_id": resource_id,
                "contact_info_id": contact_info_id,
            },
        )

    def get_contact_info_by_resource_id(
        self,
        resource_id: str,
    ) -> List[ContactInfoModel]:
        """
        获取资源的联系方式
        :param resource_id:
        :return:
        """

        sql = """
        select sci.category, sci.detail
        from st_resource_contact_info sri 
        inner join st_contact_info sci on sci.id = sri.contact_info_id
        where resource_id = :resource_id
        order by sci.category DESC
        """
        return self._fetch_all_to_model(
            model_cls=ContactInfoModel,
            sql=sql,
            params={"resource_id": resource_id},
        )

    def get_resource_contact_info(
        self,
        resource_category: str,
        resource_id: str,
        category_list: List[str],
    ) -> List[ResourceContactInfoModel]:
        """
        获取资源联系方式
        :param resource_category:
        :param resource_id:
        :param category_list:
        :return:
        """

        sql = """
        SELECT srci.id, srci.resource_category, srci.resource_id, srci.contact_info_id 
        FROM st_resource_contact_info srci
        INNER JOIN st_contact_info sci ON sci.id = srci.contact_info_id
        WHERE srci.resource_category = :resource_category
        AND srci.resource_id = :resource_id
        AND sci.category = ANY(:category_list)
        """

        return self._fetch_all_to_model(
            model_cls=ResourceContactInfoModel,
            sql=sql,
            params={
                "resource_category": resource_category,
                "resource_id": resource_id,
                "category_list": category_list,
            },
        )
