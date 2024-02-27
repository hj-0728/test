from typing import List, Set

from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction
from infra_utility.datetime_helper import local_now

from domain_evaluation.model.benchmark_input_node_model import (
    BenchmarkInputNodeModel,
    BenchmarkInputNodeSourceExecMode,
)
from domain_evaluation.model.edit.input_score_log_em import InputScoreLogEditModel
from domain_evaluation.model.edit.load_filler_em import LoadFillerEditModel
from domain_evaluation.model.edit.save_todo_task_em import SaveTodoTaskEditModel
from domain_evaluation.model.evaluation_assignment_model import EvaluationAssignmentModel
from domain_evaluation.model.evaluation_criteria_plan_model import EvaluationCriteriaPlanModel
from domain_evaluation.model.input_score_log_model import (
    EnumInputScoreLogStatus,
    InputScoreLogModel,
)
from domain_evaluation.model.todo_task_model import EnumTodoTaskTriggerCategory, EnumTodoTaskAssignCategory
from domain_evaluation.repository.benchmark_execute_node_repository import (
    BenchmarkExecuteNodeRepository,
)
from domain_evaluation.repository.benchmark_input_node_repository import BenchmarkInputNodeRepository
from domain_evaluation.repository.evaluation_assignment_repository import EvaluationAssignmentRepository
from domain_evaluation.repository.evaluation_criteria_plan_repository import EvaluationCriteriaPlanRepository
from domain_evaluation.repository.input_score_log_repository import InputScoreLogRepository
from domain_evaluation.service.benchmark_manage_service import BenchmarkManageService
from domain_evaluation.service.todo_task_service import TodoTaskService
from infra_backbone.model.role_model import EnumRoleCode
from infra_backbone.repository.role_repository import RoleRepository


class InputScoreLogService:
    """
    输入分数的日志 service
    """

    def __init__(
        self,
        input_score_log_repository: InputScoreLogRepository,
        benchmark_manage_service: BenchmarkManageService,
        benchmark_execute_node_repository: BenchmarkExecuteNodeRepository,
        benchmark_input_node_repository: BenchmarkInputNodeRepository,
        evaluation_criteria_plan_repository: EvaluationCriteriaPlanRepository,
        evaluation_assignment_repository: EvaluationAssignmentRepository,
        todo_task_service: TodoTaskService,
        role_repository: RoleRepository,
    ):
        self.__input_score_log_repository = input_score_log_repository
        self.__benchmark_manage_service = benchmark_manage_service
        self.__benchmark_execute_node_repository = benchmark_execute_node_repository
        self.__benchmark_input_node_repository = benchmark_input_node_repository
        self.__evaluation_criteria_plan_repository = evaluation_criteria_plan_repository
        self.__evaluation_assignment_repository = evaluation_assignment_repository
        self.__todo_task_service = todo_task_service
        self.__role_repository = role_repository

    def save_plan_input_score_log(
        self,
        evaluation_criteria_plan: EvaluationCriteriaPlanModel,
        evaluation_assignment_list: List[EvaluationAssignmentModel],
        transaction: Transaction,
    ):
        """
        初始化输入分数的日志
        :param evaluation_criteria_plan:
        :param evaluation_assignment_list:
        :param transaction:
        :return:
        """
        benchmark_input_node_list = self.__benchmark_input_node_repository.get_benchmark_input_node_by_evaluation_criteria_id(
            evaluation_criteria_id=evaluation_criteria_plan.evaluation_criteria_id
        )
        if len(benchmark_input_node_list) == 0:
            raise BusinessError("未找到评价标准输入节点的数据。")

        title_list = set()
        for evaluation_assignment in evaluation_assignment_list:
            for benchmark_input_node in benchmark_input_node_list:
                if (
                    benchmark_input_node.source_exec_mode
                    == BenchmarkInputNodeSourceExecMode.ONCE.name
                ):
                    try:
                        self.save_input_score_log(
                            evaluation_criteria_plan=evaluation_criteria_plan,
                            evaluation_assignment=evaluation_assignment,
                            benchmark_input_node=benchmark_input_node,
                            transaction=transaction,
                        )
                    except BusinessError as err:
                        title_list.add(str(err))

        self.save_plan_todo_task(
            title_list=title_list,
            plan_id=evaluation_criteria_plan.id,
            transaction=transaction,
        )

    def save_input_score_log(
        self,
        evaluation_criteria_plan: EvaluationCriteriaPlanModel,
        evaluation_assignment: EvaluationAssignmentModel,
        benchmark_input_node: BenchmarkInputNodeModel,
        transaction: Transaction,
    ):
        """
        保存输入分数的日志
        :param evaluation_criteria_plan:
        :param evaluation_assignment:
        :param benchmark_input_node:
        :param transaction:
        :return:
        """
        load_filler_em = LoadFillerEditModel(
            filler_calc_method=benchmark_input_node.filler_calc_method,
            benchmark_input_node_id=benchmark_input_node.id,
            establishment_assign_id=evaluation_assignment.effected_id,
        )
        expected_filler_resource_list = self.__benchmark_manage_service.load_benchmark_filler(
            params=load_filler_em
        )
        for expected_filler_resource in expected_filler_resource_list:
            input_score_log = InputScoreLogModel(
                evaluation_assignment_id=evaluation_assignment.id,
                benchmark_input_node_id=benchmark_input_node.id,
                generated_at=local_now(),
                expected_filler_category=expected_filler_resource.category,
                expected_filler_id=expected_filler_resource.id,
                fill_start_at=evaluation_criteria_plan.executed_start_at,
                fill_finish_at=evaluation_criteria_plan.executed_finish_at,
                status=EnumInputScoreLogStatus.READY.name,
            )
            self.__input_score_log_repository.insert_input_score_log(
                data=input_score_log, transaction=transaction
            )

    def update_input_score_log(
        self,
        db_input_score_log: InputScoreLogModel,
        input_score_log_em: InputScoreLogEditModel,
        transaction: Transaction,
    ):
        """
        更新分数的日志
        :param db_input_score_log:
        :param input_score_log_em:
        :param transaction:
        :return:
        """
        ec_plan = self.__evaluation_criteria_plan_repository.get_evaluation_criteria_plan_vm_by_plan_id(
            evaluation_criteria_plan_id=input_score_log_em.evaluation_criteria_plan_id
        )
        if ec_plan.executed_start_at > local_now() or ec_plan.executed_finish_at < local_now():
            raise BusinessError("不在评价标准的执行时间内。")

        db_input_score_log.to_update_data(input_score_log_em=input_score_log_em)
        return self.__input_score_log_repository.update_input_score_log(
            data=db_input_score_log,
            transaction=transaction,
            limited_col_list=['filler_id', 'filler_category', 'filled_at', 'numeric_score', 'string_score']
        )

    def regenerate_input_score_log(
        self,
        benchmark_id: str,
        plan_list: List[EvaluationCriteriaPlanModel],
        transaction: Transaction
    ):
        """
        重新生成输入日志
        """
        plan_dict = {}
        plan_ids = []
        for plan in plan_list:
            plan_ids.append(plan.id)
            plan_dict[plan.id] = plan

        assignment_list = self.__evaluation_assignment_repository.fetch_evaluation_assignment_by_plan_ids(
            plan_ids=plan_ids
        )
        input_node_list = self.__benchmark_execute_node_repository.fetch_benchmark_input_node_list(
            benchmark_id=benchmark_id
        )
        for assignment in assignment_list:
            plan = plan_dict[assignment.evaluation_criteria_plan_id]
            title_list = set()
            for input_node in input_node_list:
                try:
                    self.save_input_score_log(
                        evaluation_criteria_plan=plan,
                        evaluation_assignment=assignment,
                        benchmark_input_node=input_node,
                        transaction=transaction,
                    )
                except Exception as err:
                    title_list.add(str(err))

            self.save_plan_todo_task(
                title_list=title_list,
                plan_id=plan.id,
                transaction=transaction,
            )

    def save_plan_todo_task(self, title_list: Set[str], plan_id: str, transaction: Transaction):
        """
        保存计划的待办事项
        """
        if title_list:
            role = self.__role_repository.get_role_by_code(code=EnumRoleCode.ADMIN.name)
            todo_task = SaveTodoTaskEditModel(
                title_list=list(title_list),
                trigger_category=EnumTodoTaskTriggerCategory.EVALUATION_CRITERIA_PLAN.name,
                trigger_id=plan_id,
                assign_category=EnumTodoTaskAssignCategory.ROLE.name,
                assign_id=role.id,
            )
            self.__todo_task_service.save_todo_task(
                todo_task=todo_task,
                plan_id=plan_id,
                transaction=transaction,
            )
