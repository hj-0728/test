from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_backbone.entity.identity_number import IdentityNumberEntity
from infra_backbone.model.identity_number_model import IdentityNumberModel


class IdentityNumberRepository(BasicRepository):
    def insert_identity_number(self, data: IdentityNumberModel, transaction: Transaction) -> str:
        """
        插入证件信息
        :param data:
        :param transaction:
        :return:
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=IdentityNumberEntity, entity_model=data, transaction=transaction
        )
