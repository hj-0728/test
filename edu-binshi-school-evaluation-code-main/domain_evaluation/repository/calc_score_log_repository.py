from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from domain_evaluation.entity.calc_score_log import CalcScoreLogEntity
from domain_evaluation.model.calc_score_log_model import CalcScoreLogModel


class CalcScoreLogRepository(BasicRepository):
    """
    计算节点得分记录 Repository
    """

    def insert_calc_score_log(
        self,
        calc_score_log: CalcScoreLogModel,
        transaction: Transaction,
    ) -> str:
        """
        插入计算节点得分记录
        :param calc_score_log:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=CalcScoreLogEntity, entity_model=calc_score_log, transaction=transaction
        )
