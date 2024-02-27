from infra_basic.transaction import Transaction

from infra_backbone.model.address_model import AddressModel
from infra_backbone.model.address_relationship_model import AddressRelationshipModel
from infra_backbone.repository.address_repository import AddressRepository


class AddressService:
    def __init__(self, address_repository: AddressRepository):
        self.__address_repository = address_repository

    def add_address_with_link_resource(self, data: AddressModel, transaction: Transaction):
        """
        添加资源并关联资源
        :param data:
        :param transaction:
        :return:
        """
        self.add_address(data=data, transaction=transaction)
        if data.link_resource:
            address_relationship = data.prepare_address_relationship()
            self.link_resource(address_relationship=address_relationship, transaction=transaction)

    def add_address(self, data: AddressModel, transaction: Transaction) -> str:
        """
        添加地址
        :param data:
        :param transaction:
        :return:
        """
        same_address = self.__address_repository.fetch_address(
            area_id=data.area_id, detail=data.detail
        )
        if same_address:
            return same_address.id
        return self.__address_repository.insert_address(data=data, transaction=transaction)

    def link_resource(
        self, address_relationship: AddressRelationshipModel, transaction: Transaction
    ):
        """
        地址与资源关联
        :param address_relationship:
        :param transaction:
        :return:
        """
        self.__address_repository.insert_address_resource(
            data=address_relationship, transaction=transaction
        )

    def add_address_relationship(
        self, address_relationship: AddressRelationshipModel, transaction: Transaction
    ):
        """
        添加地址关系
        """
        existed_address_relationship = (
            self.__address_repository.get_existed_address_relationship_by_resource_and_relationship(
                resource_id=address_relationship.resource_id,
                resource_category=address_relationship.resource_category,
                relationship=address_relationship.relationship,
            )
        )
        if existed_address_relationship:
            existed_address_relationship.address_id = address_relationship.address_id
            return self.__address_repository.update_resource_address_id(
                entity_id=existed_address_relationship.id,
                version=existed_address_relationship.version,
                data=existed_address_relationship,
                transaction=transaction,
            )
        return self.__address_repository.insert_address_resource(
            data=address_relationship, transaction=transaction
        )
