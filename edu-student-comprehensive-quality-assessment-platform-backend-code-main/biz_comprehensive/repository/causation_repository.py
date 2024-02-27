from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from biz_comprehensive.entity.causation import CausationEntity
from biz_comprehensive.model.causation_model import CausationModel


class CausationRepository(BasicRepository):
    def insert_causation(self, data: CausationModel, transaction: Transaction) -> str:
        """
        插入因果关系
        :param data:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=CausationEntity, entity_model=data, transaction=transaction
        )
