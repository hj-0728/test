from typing import List

from infra_basic.transaction import Transaction

from domain_evaluation.model.calc_score_log_model import CalcScoreLogModel
from domain_evaluation.model.evaluation_assignment_model import EvaluationAssignmentModel
from domain_evaluation.repository.benchmark_execute_node_repository import \
    BenchmarkExecuteNodeRepository
from domain_evaluation.repository.calc_score_log_repository import CalcScoreLogRepository
from domain_evaluation.repository.evaluation_assignment_repository import \
    EvaluationAssignmentRepository
from domain_evaluation.repository.evaluation_criteria_plan_repository import (
    EvaluationCriteriaPlanRepository,
)
from domain_evaluation.repository.evaluation_criteria_repository import EvaluationCriteriaRepository


class CalcScoreLogService:
    """
    计算节点得分记录 service
    """

    def __init__(
        self,
        calc_score_log_repository: CalcScoreLogRepository,
        evaluation_criteria_repository: EvaluationCriteriaRepository,
        evaluation_criteria_plan_repository: EvaluationCriteriaPlanRepository,
        evaluation_assignment_repository: EvaluationAssignmentRepository,
        benchmark_execute_node_repository: BenchmarkExecuteNodeRepository,
    ):
        self.__calc_score_log_repository = calc_score_log_repository
        self.__evaluation_criteria_repository = evaluation_criteria_repository
        self.__evaluation_criteria_plan_repository = evaluation_criteria_plan_repository
        self.__evaluation_assignment_repository = evaluation_assignment_repository
        self.__benchmark_execute_node_repository = benchmark_execute_node_repository

    def save_calc_score_log(
        self,
        evaluation_criteria_id: str,
        evaluation_assignment_list: List[EvaluationAssignmentModel],
        transaction: Transaction,
    ):
        """
        保存计算节点得分记录
        :param evaluation_criteria_id:
        :param evaluation_assignment_list:
        :param transaction:
        :return:
        """

        benchmark_calc_node_list = self.__evaluation_criteria_repository.fetch_benchmark_calc_node_by_evaluation_criteria_id(
            evaluation_criteria_id=evaluation_criteria_id,
        )

        for evaluation_assignment in evaluation_assignment_list:
            for benchmark_calc_node in benchmark_calc_node_list:
                self.__calc_score_log_repository.insert_calc_score_log(
                    calc_score_log=CalcScoreLogModel(
                        evaluation_assignment_id=evaluation_assignment.id,
                        benchmark_calc_node_id=benchmark_calc_node.id,
                    ),
                    transaction=transaction,
                )

    def save_plan_calc_score_log(
        self, plan_id_list: List[str], benchmark_id: str, transaction: Transaction
    ):
        """
        保存计划的计算log
        :param plan_id_list:
        :param benchmark_id:
        :param transaction:
        :return:
        """

        evaluation_assignment_list = self.__evaluation_assignment_repository.fetch_evaluation_assignment_by_plan_ids(
            plan_ids=plan_id_list,
        )

        calc_node_list = self.__benchmark_execute_node_repository.fetch_benchmark_calc_node_list(
            benchmark_id=benchmark_id
        )

        for evaluation_assignment in evaluation_assignment_list:
            for calc_node in calc_node_list:
                self.__calc_score_log_repository.insert_calc_score_log(
                    calc_score_log=CalcScoreLogModel(
                        evaluation_assignment_id=evaluation_assignment.id,
                        benchmark_calc_node_id=calc_node.id,
                    ),
                    transaction=transaction,
                )

