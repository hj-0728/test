from typing import List

from infra_basic.transaction import Transaction
from infra_utility.datetime_helper import local_now

from backend.repository.app_establishment_assignment_repository import (
    AppEstablishmentAssignmentRepository,
)
from domain_evaluation.model.evaluation_assignment_model import (
    EnumEvaluationAssignmentEffectedCategory,
    EvaluationAssignmentModel,
)
from domain_evaluation.model.evaluation_criteria_model import EnumEvaluationObjectCategory
from domain_evaluation.model.evaluation_criteria_plan_model import EvaluationCriteriaPlanModel
from domain_evaluation.model.evaluation_criteria_plan_scope_model import (
    EnumGroupCategory,
    EvaluationCriteriaPlanScopeModel,
)
from domain_evaluation.repository.benchmark_execute_node_repository import (
    BenchmarkExecuteNodeRepository,
)
from domain_evaluation.repository.evaluation_assignment_repository import (
    EvaluationAssignmentRepository,
)
from domain_evaluation.repository.evaluation_criteria_repository import EvaluationCriteriaRepository
from domain_evaluation.service.calc_score_log_service import CalcScoreLogService
from domain_evaluation.service.evaluation_assignment_service import EvaluationAssignmentService
from domain_evaluation.service.input_score_log_service import InputScoreLogService


class AppEvaluationAssignmentService:
    """
    评价分配 service
    """

    def __init__(
        self,
        evaluation_assignment_service: EvaluationAssignmentService,
        app_establishment_assignment_repository: AppEstablishmentAssignmentRepository,
        benchmark_execute_node_repository: BenchmarkExecuteNodeRepository,
        input_score_log_service: InputScoreLogService,
        calc_score_log_service: CalcScoreLogService,
        evaluation_criteria_repository: EvaluationCriteriaRepository,
        evaluation_assignment_repository: EvaluationAssignmentRepository,
    ):
        self.__evaluation_assignment_service = evaluation_assignment_service
        self.__app_establishment_assignment_repository = app_establishment_assignment_repository
        self.__benchmark_execute_node_repository = benchmark_execute_node_repository
        self.__input_score_log_service = input_score_log_service
        self.__calc_score_log_service = calc_score_log_service
        self.__evaluation_criteria_repository = evaluation_criteria_repository
        self.__evaluation_assignment_repository = evaluation_assignment_repository

    def save_evaluation_assignment_relationship(
        self,
        evaluation_criteria_plan: EvaluationCriteriaPlanModel,
        evaluation_criteria_plan_scope_list: List[EvaluationCriteriaPlanScopeModel],
        transaction: Transaction,
    ):
        """
        保存评价分配相关
        :param evaluation_criteria_plan:
        :param evaluation_criteria_plan_scope_list:
        :param transaction:
        :return:
        """
        # 目前按照once的做，只有一次是页面点击生成，只要在计划时间内都可以。
        evaluation_criteria = (
            self.__evaluation_criteria_repository.get_evaluation_criteria_by_id(
                evaluation_criteria_id=evaluation_criteria_plan.evaluation_criteria_id
            )
        )

        # 比较之前生成的跟新修改的
        evaluation_assignment_list = self.compare_evaluation_assignment(
            evaluation_criteria_plan_id=evaluation_criteria_plan.id,
            evaluation_criteria_plan_scope_list=evaluation_criteria_plan_scope_list,
            evaluation_object_category=evaluation_criteria.evaluation_object_category,
            transaction=transaction,
        )

        self.__input_score_log_service.save_plan_input_score_log(
            evaluation_criteria_plan=evaluation_criteria_plan,
            evaluation_assignment_list=evaluation_assignment_list,
            transaction=transaction,
        )

        self.__calc_score_log_service.save_calc_score_log(
            evaluation_criteria_id=evaluation_criteria_plan.evaluation_criteria_id,
            evaluation_assignment_list=evaluation_assignment_list,
            transaction=transaction,
        )

    def compare_evaluation_assignment(
        self,
        evaluation_criteria_plan_id: str,
        evaluation_criteria_plan_scope_list: List[EvaluationCriteriaPlanScopeModel],
        evaluation_object_category: str,
        transaction: Transaction,
    ) -> List[EvaluationAssignmentModel]:
        """
        比较同个评价标准计划下的评价分配
        :param evaluation_criteria_plan_id:
        :param evaluation_criteria_plan_scope_list:
        :param evaluation_object_category:
        :param transaction:
        :return:
        """
        new_evaluation_assignment_list = []
        evaluation_assignment_list = (
            self.__evaluation_assignment_repository.get_evaluation_assignment_list_by_plan_id(
                evaluation_criteria_plan_id=evaluation_criteria_plan_id
            )
        )

        dept_id_list = [
            x.scope_id
            for x in evaluation_criteria_plan_scope_list
            if x.scope_category == EnumGroupCategory.DEPT.name
        ]
        personal_id_list = [
            x.scope_id
            for x in evaluation_criteria_plan_scope_list
            if x.scope_category == EnumGroupCategory.PERSONAL.name
        ]
        if len(dept_id_list) == 0 and len(personal_id_list) == 0:
            new_establishment_assignment_list = []
        else:
            new_establishment_assignment_list = self.__app_establishment_assignment_repository.get_establishment_assignment_list_by_plan_scope(
                evaluation_object_category=evaluation_object_category,
                dept_id_list=dept_id_list,
                personal_id_list=personal_id_list,
            )

        # 新的评价标准计划适用的集合编制分配对象跟之前已评价分配的数据进行比较：若已有则不操作，若没有则新加。
        # 根据evaluation_object_category得知评价分配的对象是谁，目前只考虑学生，教师跟学生都是使用编制分配。
        if evaluation_object_category in [
            EnumEvaluationObjectCategory.STUDENT.name,
            EnumEvaluationObjectCategory.TEACHER.name,
        ]:
            effected_id_list = [
                x.effected_id
                for x in evaluation_assignment_list
                if x.effected_category
                == EnumEvaluationAssignmentEffectedCategory.ESTABLISHMENT_ASSIGN.name
            ]
            for new_establishment_assignment in new_establishment_assignment_list:
                if new_establishment_assignment.id not in effected_id_list:
                    new_evaluation_assignment_list.append(
                        self.__evaluation_assignment_service.save_evaluation_assignment(
                            evaluation_criteria_plan_id=evaluation_criteria_plan_id,
                            establishment_assignment_id=new_establishment_assignment.id,
                            transaction=transaction,
                        )
                    )

        # 已分配的数据不在新的评价标准计划适用的集合编制分配对象内，则加上结束时间。
        new_establishment_assignment_id_list = [x.id for x in new_establishment_assignment_list]
        for evaluation_assignment in evaluation_assignment_list:
            if evaluation_assignment.effected_id not in new_establishment_assignment_id_list:
                evaluation_assignment.finish_at = local_now()
                self.__evaluation_assignment_repository.update_evaluation_assignment(
                    data=evaluation_assignment,
                    transaction=transaction,
                    limited_col_list=["finish_at"],
                )

        return new_evaluation_assignment_list
