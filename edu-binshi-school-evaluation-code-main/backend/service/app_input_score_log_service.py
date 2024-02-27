from infra_basic.basic_resource import BasicResource
from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction
from loguru import logger

from backend.model.edit.command_generate_input_score_log_em import (
    CommandGenerateInputScoreLogEditModel,
)
from backend.model.edit.save_benchmark_score_em import SaveBenchmarkScoreEm
from backend.model.view.assignment_input_score_log_vm import AssignmentInputScoreLogViewModel
from backend.repository.app_input_score_log_repository import AppInputScoreLogRepository
from domain_evaluation.model.edit.input_score_log_em import InputScoreLogEditModel
from domain_evaluation.model.edit.load_filler_em import LoadFillerEditModel
from domain_evaluation.model.evaluation_criteria_plan_model import EvaluationCriteriaPlanModel
from domain_evaluation.model.input_score_log_model import EnumExpectedFillerCategory, InputScoreLogModel, \
    EnumInputScoreLogStatus
from domain_evaluation.repository.benchmark_repository import BenchmarkRepository
from domain_evaluation.repository.input_score_log_repository import InputScoreLogRepository
from domain_evaluation.service.benchmark_manage_service import BenchmarkManageService
from domain_evaluation.service.input_score_log_service import InputScoreLogService
from infra_backbone.repository.team_member_repository import TeamMemberRepository
from collections import defaultdict


class AppInputScoreLogService:
    """
    输入分数的日志 app service
    """

    def __init__(
        self,
        input_score_log_repository: InputScoreLogRepository,
        input_score_log_service: InputScoreLogService,
        team_member_repository: TeamMemberRepository,
        benchmark_repository: BenchmarkRepository,
        app_input_score_log_repository: AppInputScoreLogRepository,
        benchmark_manage_service: BenchmarkManageService,
    ):
        self.__input_score_log_repository = input_score_log_repository
        self.__team_member_repository = team_member_repository
        self.__input_score_log_service = input_score_log_service
        self.__benchmark_repository = benchmark_repository
        self.__app_input_score_log_repository = app_input_score_log_repository
        self.__benchmark_manage_service = benchmark_manage_service

    def update_input_score_log(
        self,
        input_score_log_em: InputScoreLogEditModel,
        transaction: Transaction,
    ) -> SaveBenchmarkScoreEm:
        """
        更新分数的日志
        :param input_score_log_em:
        :param transaction:
        :return:
        """
        db_input_score_log = self.__input_score_log_repository.get_input_score_log_by_id(
            input_score_log_id=input_score_log_em.id
        )
        benchmark = self.__benchmark_repository.fetch_benchmark_by_input_node_id(
            input_node_id=db_input_score_log.benchmark_input_node_id
        )
        if not benchmark:
            raise BusinessError("未找到对应的基准。")
        if db_input_score_log.expected_filler_category == EnumExpectedFillerCategory.TEAM.name:
            team_member_list = self.__team_member_repository.get_team_member_by_team_and_people_id(
                team_id=db_input_score_log.expected_filler_id,
                people_id=input_score_log_em.people_id,
            )
            if len(team_member_list) == 0:
                raise BusinessError("您已不在该小组，无法点评。")
        self.__input_score_log_service.update_input_score_log(
            db_input_score_log=db_input_score_log,
            input_score_log_em=input_score_log_em,
            transaction=transaction,
        )
        return SaveBenchmarkScoreEm(
            benchmark_id=benchmark.id,
            evaluation_assignment_id=db_input_score_log.evaluation_assignment_id,
        )

    def handle_generate_input_score_log(
        self, data: CommandGenerateInputScoreLogEditModel, transaction: Transaction
    ):
        """
        处理pubsub推送过来需要再生成输入日志的消息
        """
        benchmark_plan_list = self.__app_input_score_log_repository.fetch_benchmark_plan_list(
            trigger_category=data.trigger_category, trigger_ids=data.trigger_ids
        )
        plan_todo_title_dict = defaultdict(set)
        total_benchmark_plan_count = len(benchmark_plan_list)
        for idx, benchmark in enumerate(benchmark_plan_list, start=1):
            logger.info(f"001====>>正在处理第{idx}/{total_benchmark_plan_count}个基准的填写日志")
            plan_dict = benchmark.plan_dict()
            assignment_list = self.__app_input_score_log_repository.fetch_evaluation_assignment(
                plan_ids=benchmark.plan_ids(), input_node_id=benchmark.benchmark_input_node_id
            )
            logger.info(f"002====>>第{idx}/{total_benchmark_plan_count}个基准的评价分配共有{len(assignment_list)}个")
            for assignment in assignment_list:
                try:
                    load_filler_em = LoadFillerEditModel(
                        filler_calc_method=benchmark.filler_calc_method,
                        benchmark_input_node_id=benchmark.benchmark_input_node_id,
                        establishment_assign_id=assignment.evaluation_assignment.effected_id,
                    )
                    try:
                        filler_list = self.__benchmark_manage_service.load_benchmark_filler(
                            params=load_filler_em
                        )
                        if not filler_list:
                            raise BusinessError("未找到填写者")
                    except Exception as err:
                        plan_todo_title_dict[assignment.evaluation_assignment.evaluation_criteria_plan_id].add(
                            str(err)
                        )
                        logger.error(f"加载基准填写者失败，原因：{err}")
                    else:
                        self.update_evaluation_assignment_input_score_log(
                            assignment=assignment,
                            new_filler=filler_list[0],  # 目前的场景都只有一个填写者
                            benchmark_input_node_id=benchmark.benchmark_input_node_id,
                            plan=plan_dict[assignment.evaluation_assignment.evaluation_criteria_plan_id],
                            transaction=transaction,
                        )
                except Exception as err2:
                    logger.error(f"更新填写者失败，原因：{err2}")

        for plan_id, title_list in plan_todo_title_dict.items():
            self.__input_score_log_service.save_plan_todo_task(
                title_list=title_list, plan_id=plan_id, transaction=transaction
            )

    def update_evaluation_assignment_input_score_log(
        self,
        assignment: AssignmentInputScoreLogViewModel,
        new_filler: BasicResource,
        benchmark_input_node_id: str,
        plan: EvaluationCriteriaPlanModel,
        transaction: Transaction
    ):
        """
        更新评价分配的输入分数日志
        """
        if assignment.input_score_log:
            if assignment.input_score_log.expected_filler_id != new_filler.id:
                assignment.input_score_log.expected_filler_id = new_filler.id
                self.__input_score_log_repository.update_input_score_log(
                    data=assignment.input_score_log,
                    transaction=transaction,
                    limited_col_list=["expected_filler_id"],
                )
        else:
            new_input_score_log = InputScoreLogModel(
                evaluation_assignment_id=assignment.evaluation_assignment.id,
                benchmark_input_node_id=benchmark_input_node_id,
                expected_filler_category=new_filler.category,
                expected_filler_id=new_filler.id,
                fill_start_at=plan.executed_start_at,
                fill_finish_at=plan.executed_finish_at,
                status=EnumInputScoreLogStatus.READY.name,
            )
            self.__input_score_log_repository.insert_input_score_log(
                data=new_input_score_log,
                transaction=transaction,
            )
