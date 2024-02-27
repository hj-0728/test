from typing import Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_backbone.entity.address import AddressEntity
from infra_backbone.entity.address_relationship import AddressRelationshipEntity
from infra_backbone.model.address_model import AddressModel
from infra_backbone.model.address_relationship_model import AddressRelationshipModel


class AddressRepository(BasicRepository):
    def insert_address(self, data: AddressModel, transaction: Transaction) -> str:
        """
        插入地址
        :param data:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity(
            entity_cls=AddressEntity, entity_data=data.dict(), transaction=transaction
        )

    def insert_address_resource(self, data: AddressRelationshipModel, transaction: Transaction):
        """
        插入地址关联资源
        :param data:
        :param transaction:
        :return:
        """
        self._insert_versioned_entity(
            entity_cls=AddressRelationshipEntity,
            entity_data=data.dict(),
            transaction=transaction,
        )

    def fetch_address(self, area_id: str, detail: str) -> Optional[AddressModel]:
        """
        获取地址
        :param area_id:
        :param detail:
        :return:
        """

        sql = """select * from st_address where area_id = :area_id
        and detail = :detail"""
        return self._fetch_first_to_model(
            model_cls=AddressModel,
            sql=sql,
            params={"area_id": area_id, "detail": detail},
        )

    def get_existed_address_relationship_by_resource_and_relationship(
        self,
        resource_category: str,
        resource_id: str,
        relationship: Optional[str] = None,
    ):
        """
        根据关联来源和关系获取地址关联关系
        """
        sql = """
        select * from st_address_relationship
        where resource_id = :resource_id and resource_category = :resource_category
        and relationship = :relationship
        """
        return self._fetch_first_to_model(
            sql=sql,
            model_cls=AddressRelationshipModel,
            params={
                "resource_id": resource_id,
                "resource_category": resource_category,
                "relationship": relationship,
            },
        )

    def update_resource_address_id(
        self,
        entity_id: str,
        version: int,
        data: AddressRelationshipModel,
        transaction: Transaction,
    ):
        """
        更新关联关系
        """
        self._update_versioned_entity_by_dict(
            entity_cls=AddressRelationshipEntity,
            entity_id=entity_id,
            version=version,
            update_data=data.dict(),
            transaction=transaction,
            limited_col_list=["address_id"],
        )
