from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from biz_comprehensive.entity.indicator_score_log import IndicatorScoreLogEntity
from biz_comprehensive.model.indicator_score_log_model import IndicatorScoreLogModel


class IndicatorScoreLogRepository(BasicRepository):
    def insert_indicator_score_log(
        self, data: IndicatorScoreLogModel, transaction: Transaction
    ) -> str:
        """
        插入指标分数日志
        :param data:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=IndicatorScoreLogEntity, entity_model=data, transaction=transaction
        )
