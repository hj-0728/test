from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from biz_comprehensive.entity.medal_issued_log import MedalIssuedLogEntity
from biz_comprehensive.model.medal_issued_log_model import MedalIssuedLogModel


class MedalIssuedLogRepository(BasicRepository):
    def insert_medal_issued_log(self, data: MedalIssuedLogModel, transaction: Transaction) -> str:
        """
        插入勋章发放日志
        :param data:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=MedalIssuedLogEntity, entity_model=data, transaction=transaction
        )
