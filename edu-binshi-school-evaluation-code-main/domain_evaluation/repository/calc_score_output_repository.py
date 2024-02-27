from typing import List

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from domain_evaluation.entity.calc_score_output import CalcScoreOutputEntity
from domain_evaluation.model.calc_score_output_model import CalcScoreOutputModel


class CalcScoreOutputRepository(BasicRepository):
    """
    计算节点输出 Repository
    """

    def insert_calc_score_output(
        self,
        calc_score_output: CalcScoreOutputModel,
        transaction: Transaction,
    ) -> str:
        """
        插入计算节点输出
        :param calc_score_output:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=CalcScoreOutputEntity,
            entity_model=calc_score_output,
            transaction=transaction,
        )

    def delete_calc_score_output(
        self,
        calc_score_output_id: str,
        transaction: Transaction,
    ):
        """
        删除 计算节点输出
        :param calc_score_output_id:
        :param transaction:
        :return:
        """

        return self._delete_versioned_entity_by_id(
            entity_cls=CalcScoreOutputEntity,
            entity_id=calc_score_output_id,
            transaction=transaction
        )

    def get_calc_score_output_by_log_id(
        self, calc_score_log_id: str
    ) -> List[CalcScoreOutputModel]:
        """
        根据 calc_score_log_id 获取 计算节点输出
        :param calc_score_log_id:
        :return:
        """

        sql = """
        select * from st_calc_score_output 
        where calc_score_log_id=:calc_score_log_id
        """

        return self._fetch_all_to_model(
            sql=sql,
            model_cls=CalcScoreOutputModel,
            params={
                "calc_score_log_id": calc_score_log_id
            }
        )

