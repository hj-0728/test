from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction

from backend.service.app_evaluation_assignment_service import AppEvaluationAssignmentService
from backend.service.app_evaluation_criteria_plan_scope_service import (
    AppEvaluationCriteriaPlanScopeService,
)
from domain_evaluation.model.evaluation_criteria_plan_model import (
    SaveEvaluationCriteriaPlanAndScopeModel,
)
from domain_evaluation.repository.evaluation_criteria_plan_repository import EvaluationCriteriaPlanRepository
from domain_evaluation.service.evaluation_criteria_plan_service import EvaluationCriteriaPlanService


class AppEvaluationCriteriaPlanService:
    def __init__(
        self,
        evaluation_criteria_plan_service: EvaluationCriteriaPlanService,
        app_evaluation_criteria_plan_scope_service: AppEvaluationCriteriaPlanScopeService,
        evaluation_criteria_plan_repository: EvaluationCriteriaPlanRepository,
        app_evaluation_assignment_service: AppEvaluationAssignmentService,
    ):
        self.__evaluation_criteria_plan_service = evaluation_criteria_plan_service
        self.__app_evaluation_criteria_plan_scope_service = (
            app_evaluation_criteria_plan_scope_service
        )
        self.__evaluation_criteria_plan_repository = evaluation_criteria_plan_repository
        self.__app_evaluation_assignment_service = app_evaluation_assignment_service

    def save_evaluation_criteria_plan_and_scope(
        self, data: SaveEvaluationCriteriaPlanAndScopeModel, transaction: Transaction
    ):
        """
        保存评价标准计划和计划适用范围
        :param data:
        :param transaction:
        """
        evaluation_criteria_plan = None

        if data.evaluation_criteria_plan:
            exist_evaluation_criteria_plan = (
                self.__evaluation_criteria_plan_service.get_evaluation_criteria_plan_by_name(
                    name=data.evaluation_criteria_plan.name
                )
            )
            if (
                exist_evaluation_criteria_plan
                and exist_evaluation_criteria_plan.id != data.evaluation_criteria_plan.id
            ):
                raise BusinessError("已存在同名计划，请修改后重试")

            evaluation_criteria_plan = (
                self.__evaluation_criteria_plan_service.save_evaluation_criteria_plan(
                    evaluation_criteria_plan=data.evaluation_criteria_plan, transaction=transaction
                )
            )

        if data.evaluation_criteria_plan_scope:
            if evaluation_criteria_plan is not None:
                evaluation_criteria_plan = (
                    evaluation_criteria_plan.to_evaluation_criteria_plan_model()
                )
            evaluation_criteria_plan_vm, evaluation_criteria_plan_scope_list = \
                self.__app_evaluation_criteria_plan_scope_service.save_evaluation_criteria_plan_scope(
                    data=data.evaluation_criteria_plan_scope,
                    evaluation_criteria_plan=evaluation_criteria_plan,
                    transaction=transaction,
                )

            return evaluation_criteria_plan_vm, evaluation_criteria_plan_scope_list

    def refresh_evaluation_criteria_plan_data(self, transaction: Transaction):
        """
        同步之后更新计划相关的评价分配、分数录入日志等
        """
        plan_list = self.__evaluation_criteria_plan_repository.fetch_executing_plan_scope()
        for plan in plan_list:
            self.__app_evaluation_assignment_service.save_evaluation_assignment_relationship(
                evaluation_criteria_plan=plan.plan,
                evaluation_criteria_plan_scope_list=plan.scope_list,
                transaction=transaction,
            )
