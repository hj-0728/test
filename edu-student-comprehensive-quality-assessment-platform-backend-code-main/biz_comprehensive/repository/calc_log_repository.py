from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from biz_comprehensive.entity.calc_log import CalcLogEntity
from biz_comprehensive.model.calc_log_model import CalcLogModel


class CalcLogRepository(BasicRepository):
    def insert_calc_log(self, data: CalcLogModel, transaction: Transaction) -> str:
        """
        插入计算日志
        :param data:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=CalcLogEntity, entity_model=data, transaction=transaction
        )
