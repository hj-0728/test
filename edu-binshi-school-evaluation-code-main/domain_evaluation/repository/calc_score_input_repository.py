from typing import List

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from domain_evaluation.entity.calc_score_input import CalcScoreInputEntity
from domain_evaluation.model.calc_score_input_model import CalcScoreInputModel


class CalcScoreInputRepository(BasicRepository):
    """
    计算节点来源 Repository
    """

    def insert_calc_score_input(
        self,
        calc_score_input: CalcScoreInputModel,
        transaction: Transaction,
    ) -> str:
        """
        插入计算节点来源
        :param calc_score_input:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=CalcScoreInputEntity, entity_model=calc_score_input, transaction=transaction
        )

    def delete_calc_score_input(
        self,
        calc_score_input_id: str,
        transaction: Transaction,
    ):
        """
        删除 计算节点来源
        :param calc_score_input_id:
        :param transaction:
        :return:
        """

        return self._delete_versioned_entity_by_id(
            entity_cls=CalcScoreInputEntity,
            entity_id=calc_score_input_id,
            transaction=transaction
        )

    def get_calc_score_input_by_log_id(
        self, calc_score_log_id: str
    ) -> List[CalcScoreInputModel]:
        """
        根据 calc_score_log_id 获取 计算节点来源
        :param calc_score_log_id:
        :return:
        """

        sql = """
        select * from st_calc_score_input where calc_score_log_id=:calc_score_log_id
        """

        return self._fetch_all_to_model(
            sql=sql,
            model_cls=CalcScoreInputModel,
            params={
                "calc_score_log_id": calc_score_log_id
            }
        )
