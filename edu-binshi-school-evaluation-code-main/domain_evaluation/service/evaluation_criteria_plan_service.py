from typing import Optional

from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction
from infra_utility.datetime_helper import local_now
from infra_utility.enum_helper import get_enum_value_by_name

from domain_evaluation.data.query_params.evaluation_criteria_plan_query_params import (
    EvaluationCriteriaPlanQueryParams,
)
from domain_evaluation.data.query_params.evaluation_criteria_plan_stats_query_params import (
    EvaluationCriteriaPlanStatsQueryParams,
)
from domain_evaluation.model.evaluation_criteria_model import EnumEvaluationObjectCategory
from domain_evaluation.model.evaluation_criteria_plan_model import (
    EnumEvaluationCriteriaPlanStatus,
    EvaluationCriteriaPlanModel,
    SaveEvaluationCriteriaPlanModel,
)
from domain_evaluation.model.view.evaluation_criteria_plan_vm import EvaluationCriteriaPlanViewModel
from domain_evaluation.repository.evaluation_criteria_plan_repository import (
    EvaluationCriteriaPlanRepository,
)
from domain_evaluation.repository.input_score_log_repository import InputScoreLogRepository
from infra_backbone.model.role_model import EnumRoleCode


class EvaluationCriteriaPlanService:
    """
    评价标准计划 service
    """

    def __init__(
        self,
        evaluation_criteria_plan_repository: EvaluationCriteriaPlanRepository,
        input_score_log_repository: InputScoreLogRepository,
    ):
        self.__evaluation_criteria_plan_repository = evaluation_criteria_plan_repository
        self.__input_score_log_repository = input_score_log_repository

    def save_evaluation_criteria_plan(
        self,
        evaluation_criteria_plan: SaveEvaluationCriteriaPlanModel,
        transaction: Transaction,
    ):
        # 保存评价标准计划
        evaluation_criteria_plan_em = evaluation_criteria_plan.to_evaluation_criteria_plan_model()
        if evaluation_criteria_plan.id:
            # 更新
            self.__evaluation_criteria_plan_repository.update_evaluation_criteria_plan(
                evaluation_criteria_plan=evaluation_criteria_plan_em,
                transaction=transaction,
                limited_col_list=[
                    "evaluation_criteria_id",
                    "focus_period_id",
                    "name",
                    "executed_start_at",
                    "executed_finish_at",
                    "status",
                ],
            )

            input_score_log_list = self.__input_score_log_repository.get_input_score_log_by_evaluation_criteria_plan_id(
                evaluation_criteria_plan_id=evaluation_criteria_plan_em.id
            )

            for input_score_log in input_score_log_list:
                input_score_log.fill_finish_at = evaluation_criteria_plan_em.executed_finish_at
                self.__input_score_log_repository.update_input_score_log(
                    data=input_score_log,
                    transaction=transaction,
                    limited_col_list=["fill_finish_at"],
                )
        else:
            # 新增
            evaluation_criteria_plan.id = (
                self.__evaluation_criteria_plan_repository.insert_evaluation_criteria_plan(
                    evaluation_criteria_plan=evaluation_criteria_plan_em,
                    transaction=transaction,
                )
            )
        return evaluation_criteria_plan

    def get_evaluation_criteria_plan_list(self, params: EvaluationCriteriaPlanQueryParams):
        """
        获取评价计划列表
        """
        evaluation_criteria_plan_list = (
            self.__evaluation_criteria_plan_repository.get_evaluation_criteria_plan_list(
                params=params
            )
        )

        for evaluation_criteria_plan in evaluation_criteria_plan_list.data:
            evaluation_criteria_plan.status_name = get_enum_value_by_name(
                enum_class=EnumEvaluationCriteriaPlanStatus,
                enum_name=evaluation_criteria_plan.status,
            )
        return evaluation_criteria_plan_list

    def update_evaluation_criteria_plan(
        self,
        evaluation_criteria_plan: EvaluationCriteriaPlanModel,
        trans: Transaction,
    ):
        """
        作废评价计划
        :param evaluation_criteria_plan
        :param trans
        :return
        """
        self.__evaluation_criteria_plan_repository.update_evaluation_criteria_plan(
            evaluation_criteria_plan=evaluation_criteria_plan,
            transaction=trans,
            limited_col_list=["status"],
        )

    def get_evaluation_criteria_plan_detail(self, evaluation_criteria_plan_id: str):
        """
        获取评价标准计划详情
        :param evaluation_criteria_plan_id:
        :return:
        """
        return self.__evaluation_criteria_plan_repository.get_evaluation_criteria_plan_detail(
            evaluation_criteria_plan_id=evaluation_criteria_plan_id
        )

    def delete_evaluation_criteria_plan(
        self,
        evaluation_criteria_plan_id: str,
        transaction: Transaction,
    ):
        """
        删除评价标准
        :param evaluation_criteria_plan_id:
        :param transaction:
        :return:
        """

        # 删除评价标准
        self.__evaluation_criteria_plan_repository.delete_evaluation_criteria(
            evaluation_criteria_plan_id=evaluation_criteria_plan_id,
            transaction=transaction,
        )

    def get_evaluation_criteria_plan_todo_page_list(
        self, params: EvaluationCriteriaPlanStatsQueryParams, current_role_code: str
    ):
        """
        获取评价标准计划列表
        :param params:
        :param current_role_code:
        :return:
        """
        result = (
            self.__evaluation_criteria_plan_repository.get_evaluation_criteria_plan_todo_page_list(
                params=params
            )
        )

        show_report_status = [
            EnumEvaluationCriteriaPlanStatus.IN_PROGRESS.name,
            EnumEvaluationCriteriaPlanStatus.ARCHIVED.name,
        ]

        for data in result.data:
            data.evaluation_object_category_name = get_enum_value_by_name(
                enum_class=EnumEvaluationObjectCategory,
                enum_name=data.evaluation_object_category,
                fallback="未知",
            )
            data.plan_status_name = get_enum_value_by_name(
                enum_class=EnumEvaluationCriteriaPlanStatus,
                enum_name=data.plan_status,
                fallback="未知",
            )
            if (
                data.plan_status in show_report_status
                and current_role_code != EnumRoleCode.STUDENT.name
                and local_now() > data.executed_finish_at
            ):
                data.show_report = True
        return result

    def get_evaluation_criteria_plan(self, plan_id: str) -> EvaluationCriteriaPlanModel:
        """
        获取评价计划
        """
        plan = self.__evaluation_criteria_plan_repository.fetch_evaluation_criteria_plan_by_id(
            evaluation_criteria_plan_id=plan_id
        )
        plan.status_name = get_enum_value_by_name(
            enum_class=EnumEvaluationCriteriaPlanStatus,
            enum_name=plan.status,
            fallback="未知",
        )
        if not plan:
            raise BusinessError("评价计划不存在")
        return plan

    def get_evaluation_criteria_plan_by_name(
        self, name: str
    ) -> Optional[EvaluationCriteriaPlanViewModel]:
        """
        根据name获取评价标准计划
        :param name:
        :return:
        """

        return self.__evaluation_criteria_plan_repository.get_evaluation_criteria_plan_by_name(
            name=name
        )

    def archived_evaluation_criteria_plan(self, transaction: Transaction):
        """
        归档已结束的计划
        :param transaction:
        """
        finished_evaluation_criteria_plan_list = (
            self.__evaluation_criteria_plan_repository.get_finished_evaluation_criteria_plan()
        )

        for finished_evaluation_criteria_plan in finished_evaluation_criteria_plan_list:
            finished_evaluation_criteria_plan.status = (
                EnumEvaluationCriteriaPlanStatus.ARCHIVED.name
            )
            self.__evaluation_criteria_plan_repository.update_evaluation_criteria_plan(
                evaluation_criteria_plan=finished_evaluation_criteria_plan,
                transaction=transaction,
                limited_col_list=["status"],
            )
