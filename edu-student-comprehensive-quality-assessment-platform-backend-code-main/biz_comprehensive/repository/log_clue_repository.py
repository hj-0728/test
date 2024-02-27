from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from biz_comprehensive.entity.log_clue import LogClueEntity
from biz_comprehensive.model.log_clue_model import LogClueModel


class LogClueRepository(BasicRepository):
    def insert_log_clue(self, data: LogClueModel, transaction: Transaction) -> str:
        """
        插入日志线索
        :param data:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=LogClueEntity, entity_model=data, transaction=transaction
        )
