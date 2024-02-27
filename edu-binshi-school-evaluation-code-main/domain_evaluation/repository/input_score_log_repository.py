from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from domain_evaluation.entity.input_score_log import InputScoreLogEntity
from domain_evaluation.model.input_score_log_model import InputScoreLogModel


class InputScoreLogRepository(BasicRepository):
    """
    输入分数的日志 Repository
    """

    def insert_input_score_log(
        self,
        data: InputScoreLogModel,
        transaction: Transaction,
    ) -> str:
        """
        插入输入分数的日志
        :param data:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=InputScoreLogEntity, entity_model=data, transaction=transaction
        )

    def update_input_score_log(
        self,
        data: InputScoreLogModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """
        更新输入分数的日志
        :param data:
        :param transaction:
        :param limited_col_list:
        :return:
        """
        return self._update_versioned_entity_by_model(
            entity_cls=InputScoreLogEntity,
            update_model=data,
            transaction=transaction,
            limited_col_list=limited_col_list,
        )

    def get_input_score_log_by_id(
        self, input_score_log_id: str,
    ) -> Optional[InputScoreLogModel]:
        """
        获取输入分数的日志通过id
        :param input_score_log_id:
        :return:
        """
        sql = """
        select * from st_input_score_log where id = :input_score_log_id
        """
        return self._fetch_first_to_model(
            model_cls=InputScoreLogModel,
            sql=sql,
            params={
                "input_score_log_id": input_score_log_id,
            },
        )

    def get_input_score_log_by_evaluation_criteria_plan_id(
        self,
        evaluation_criteria_plan_id: str
    ) -> List[InputScoreLogModel]:
        """
        根据评价id获取输入分数的日志
        :param evaluation_criteria_plan_id:
        :return
        """
        sql = """
        SELECT sl.* FROM st_evaluation_criteria_plan cp
        INNER JOIN st_evaluation_assignment ea ON ea.evaluation_criteria_plan_id = cp.id
        INNER JOIN st_input_score_log sl ON sl.evaluation_assignment_id = ea.id
        WHERE cp.id = :evaluation_criteria_plan_id
        """
        return self._fetch_all_to_model(
            model_cls=InputScoreLogModel,
            sql=sql,
            params={
                "evaluation_criteria_plan_id": evaluation_criteria_plan_id,
            },
        )


