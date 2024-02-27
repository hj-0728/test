import logging
import time
import traceback
from typing import Any, Dict, List, Optional

from dependency_injector.wiring import inject, Provide
from infra_basic.uow_interface import UnitOfWork

from backend.backend_containers import BackendContainer
from backend.data.enum import EnumRedisFlag
from backend.model.edit.command_generate_input_score_log_em import (
    CommandGenerateInputScoreLogEditModel,
)
from backend.model.edit.save_benchmark_score_em import SaveBenchmarkScoreEm
from backend.service.app_evaluation_assignment_service import AppEvaluationAssignmentService
from backend.service.app_evaluation_criteria_plan_service import AppEvaluationCriteriaPlanService
from backend.service.app_input_score_log_service import AppInputScoreLogService
from backend.service.app_user_service import AppUserService
from backend.service.redis_service import RedisService
from domain_evaluation.model.benchmark_input_node_model import BenchmarkInputNodeSourceCategory
from domain_evaluation.model.evaluation_assignment_model import SaveEvaluationAssignmentRelationshipModel
from domain_evaluation.repository.benchmark_input_node_repository import (
    BenchmarkInputNodeRepository,
)
from domain_evaluation.repository.evaluation_assignment_repository import (
    EvaluationAssignmentRepository,
)
from domain_evaluation.repository.evaluation_criteria_plan_repository import (
    EvaluationCriteriaPlanRepository,
)
from domain_evaluation.service.benchmark_score_service import BenchmarkScoreService
from domain_evaluation.service.calc_score_log_service import CalcScoreLogService
from domain_evaluation.service.input_score_log_service import InputScoreLogService
from edu_binshi.model.report_record_model import EnumReportRecordStatus
from edu_binshi.model.view.report_record_vm import ReportRecordViewModel
from edu_binshi.repository.report_repository import ReportRepository
from edu_binshi.service.k12_teacher_subject_service import K12TeacherSubjectService
from edu_binshi.service.report_service import ReportService
from infra_backbone.model.access_log_model import AccessLogModel
from infra_backbone.service.access_log_service import AccessLogService
from infra_backbone.service.robot_service import RobotService
from infra_utility.token_helper import generate_by_host_and_time


@inject
def task_save_access_log(
    data: Dict[str, Any],
    uow: UnitOfWork = Provide[BackendContainer.uow],
    access_log_service: AccessLogService = Provide[
        BackendContainer.backbone_container.access_log_service
    ],
):
    """
    保存访问日志
    :param data:
    :param uow:
    :param access_log_service:
    :return:
    """
    try:
        with uow:
            access_log_service.save_access_log(access_log=AccessLogModel(**data))
    except Exception as error:
        logging.error(error)
        traceback.print_exc()


@inject
def task_save_benchmark_score(
    data: Dict[str, Any],
    uow: UnitOfWork = Provide[BackendContainer.uow],
    benchmark_score_service: BenchmarkScoreService = Provide[
        BackendContainer.domain_evaluation_container.benchmark_score_service
    ],
    robot_service: RobotService = Provide[BackendContainer.backbone_container.robot_service],
    evaluation_assignment_repository: EvaluationAssignmentRepository = Provide[
        BackendContainer.domain_evaluation_container.evaluation_assignment_repository
    ],
    redis_service: RedisService = Provide[BackendContainer.redis_service],
):
    """
    保存benchmark score
    :param data:
    :param uow:
    :param benchmark_score_service:
    :param robot_service:
    :param evaluation_assignment_repository:
    :param redis_service:
    :return:
    """
    try:
        key = EnumRedisFlag.FLAG_SAVE_BENCHMARK_SCORE.name
        while redis_service.exists(key):
            time.sleep(10)
        benchmark_list = []
        with uow:
            param = SaveBenchmarkScoreEm(**data)
            redis_service.set(key=key, value=param.value, ex=30*60)
            handler = robot_service.get_system_robot().to_basic_handler()
            transaction = uow.log_transaction(
                handler=handler,
                action="save_benchmark_score",
                action_params={"data": data},
            )
            try:
                benchmark_score_service.save_benchmark_score(
                    benchmark_id=param.benchmark_id,
                    evaluation_assignment_id=param.evaluation_assignment_id,
                    transaction=transaction,
                )
                benchmark_list = evaluation_assignment_repository.get_affected_benchmark_by_evaluation_assignment_id_and_benchmark_id(
                    evaluation_assignment_id=param.evaluation_assignment_id,
                    benchmark_id=param.benchmark_id,
                )
            except Exception as error:
                logging.error(error)
        redis_service.delete(key=key)
        for benchmark in benchmark_list:
            task_save_benchmark_score(
                data=SaveBenchmarkScoreEm(
                    benchmark_id=benchmark.id,
                    evaluation_assignment_id=param.evaluation_assignment_id,
                ).dict()
            )
    except Exception as error:
        logging.error(error)
        traceback.print_exc()


@inject
def task_regenerate_score_log(
    data: Dict[str, Any],
    uow: UnitOfWork = Provide[BackendContainer.uow],
    robot_service: RobotService = Provide[BackendContainer.backbone_container.robot_service],
    evaluation_criteria_plan_repository: EvaluationCriteriaPlanRepository = Provide[
        BackendContainer.domain_evaluation_container.evaluation_criteria_plan_repository
    ],
    benchmark_input_node_repository: BenchmarkInputNodeRepository = Provide[
        BackendContainer.domain_evaluation_container.benchmark_input_node_repository
    ],
    input_score_log_service: InputScoreLogService = Provide[
        BackendContainer.domain_evaluation_container.input_score_log_service
    ],
    calc_score_log_service: CalcScoreLogService = Provide[
        BackendContainer.domain_evaluation_container.calc_score_log_service
    ],
    redis_service: RedisService = Provide[BackendContainer.redis_service],
):
    try:
        key = EnumRedisFlag.FLAG_REGENERATE_SCORE_LOG.name
        while redis_service.exists(key):
            time.sleep(10)
        benchmark_id = data.get("benchmark_id")
        redis_service.set(key=key, value=benchmark_id, ex=30 * 60)
        with uow:
            handler = robot_service.get_system_robot().to_basic_handler()
            transaction = uow.log_transaction(
                handler=handler,
                action="task_regenerate_score_log",
                action_params={"data": data},
            )
            executing_plan_list = (
                evaluation_criteria_plan_repository.fetch_executing_plan_by_benchmark_id(
                    benchmark_id=benchmark_id
                )
            )
            if executing_plan_list:
                source_category = (
                    benchmark_input_node_repository.fetch_benchmark_input_node_source_category(
                        benchmark_id=benchmark_id
                    )
                )
                if source_category == BenchmarkInputNodeSourceCategory.INPUT.name:
                    input_score_log_service.regenerate_input_score_log(
                        benchmark_id=benchmark_id,
                        plan_list=executing_plan_list,
                        transaction=transaction,
                    )
                else:
                    plan_id_list = [x.id for x in executing_plan_list]
                    calc_score_log_service.save_plan_calc_score_log(
                        benchmark_id=benchmark_id,
                        plan_id_list=plan_id_list,
                        transaction=transaction,
                    )
        if (
            executing_plan_list
            and source_category == BenchmarkInputNodeSourceCategory.BENCHMARK.name
        ):
            task_save_plan_benchmark_score(
                plan_id_list=plan_id_list,
                benchmark_id=benchmark_id,
            )
        redis_service.delete(key=key)
    except Exception as error:
        logging.error(error)
        traceback.print_exc()


@inject
def task_save_plan_benchmark_score(
    plan_id_list: List[str],
    benchmark_id: str,
    uow: UnitOfWork = Provide[BackendContainer.uow],
    evaluation_assignment_repository: EvaluationAssignmentRepository = Provide[
        BackendContainer.domain_evaluation_container.evaluation_assignment_repository
    ],
):
    """
    保存计划的benchmark_score
    :param plan_id_list:
    :param benchmark_id:
    :param uow:
    :param evaluation_assignment_repository:
    :return:
    """
    with uow:
        evaluation_assignment_list = (
            evaluation_assignment_repository.fetch_evaluation_assignment_by_plan_ids(
                plan_ids=plan_id_list,
            )
        )
    for evaluation_assignment in evaluation_assignment_list:
        task_save_benchmark_score(
            data=SaveBenchmarkScoreEm(
                benchmark_id=benchmark_id,
                evaluation_assignment_id=evaluation_assignment.id,
            ).dict()
        )


@inject
def task_get_dimension_dept_tree_report(
    data: Dict[str, Any],
    uow: UnitOfWork = Provide[BackendContainer.uow],
    robot_service: RobotService = Provide[BackendContainer.backbone_container.robot_service],
    report_service: ReportService = Provide[
        BackendContainer.edu_evaluation_container.report_service
    ],
):
    try:
        with uow:
            handler = robot_service.get_system_robot().to_basic_handler()
            transaction = uow.log_transaction(
                handler=handler,
                action="task_get_dimension_dept_tree_report",
                action_params={"data": data},
            )
            file_info, report_record = report_service.generate_report(
                report_record=ReportRecordViewModel(**data),
                transaction=transaction,
            )
            if report_record:
                report_service.send_site_message(
                    args=report_record,
                    transaction=transaction,
                    file_info=file_info
                )
        task_handle_pending_report_record()

    except Exception as error:
        logging.error(error)
        traceback.print_exc()


@inject
def task_handle_pending_report_record(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    robot_service: RobotService = Provide[BackendContainer.backbone_container.robot_service],
    report_service: ReportService = Provide[
        BackendContainer.edu_evaluation_container.report_service
    ],
    report_repository: ReportRepository = Provide[
        BackendContainer.edu_evaluation_container.report_repository
    ],
):
    try:
        with uow:
            report_record_list = report_repository.get_report_record_by_status(
                status=EnumReportRecordStatus.PENDING.name
            )
            handler = robot_service.get_system_robot().to_basic_handler()
        need_handle_report_list = []
        for report_record in report_record_list:
            with uow:
                transaction = uow.log_transaction(
                    handler=handler,
                    action="task_save_report_record",
                    action_params={"data": report_record},
                )
                try:
                    report_record_info = ReportRecordViewModel(**report_record.args)
                    report_record_info.id = report_record.id
                    report_record_info.version = report_record.version
                    file_url = report_service.before_generate_report_check(
                        args=report_record,
                        transaction=transaction,
                        not_insert=False,
                    )
                    if file_url:
                        report_service.send_site_message(
                            args=report_record_info,
                            transaction=transaction,
                            file_info=file_url,
                        )
                    else:
                        need_handle_report_list.append(report_record_info)
                except Exception as error:
                    logging.error(error)
        for need_handle_report in need_handle_report_list:
            task_get_dimension_dept_tree_report(
                data=need_handle_report.dict()
            )

    except Exception as error:
        logging.error(error)
        traceback.print_exc()


@inject
def task_handle_generate_input_score_log(
    data: Dict[str, str],
    uow: UnitOfWork = Provide[BackendContainer.uow],
    robot_service: RobotService = Provide[BackendContainer.backbone_container.robot_service],
    app_input_score_log_service: AppInputScoreLogService = Provide[
        BackendContainer.app_input_score_log_service
    ],
    redis_service: RedisService = Provide[BackendContainer.redis_service],
):
    """
    保存计划的benchmark_score
    :param data:
    :param uow:
    :param robot_service:
    :param app_input_score_log_service:
    :param redis_service:
    :return:
    """
    try:
        key = EnumRedisFlag.FLAG_HANDLE_GENERATE_INPUT_SCORE_LOG.name
        while redis_service.exists(key):
            time.sleep(10)
        with uow:
            params = CommandGenerateInputScoreLogEditModel(**data)
            redis_service.set(key=key, value=params.trigger_category, ex=30 * 60)
            handler = robot_service.get_system_robot().to_basic_handler()
            transaction = uow.log_transaction(
                handler=handler,
                action="task_handle_generate_input_score_log",
                action_params={"data": data},
            )
            app_input_score_log_service.handle_generate_input_score_log(
                data=params, transaction=transaction
            )
        redis_service.delete(key=key)
    except Exception as error:
        logging.error(error)
        traceback.print_exc()


@inject
def task_refresh_evaluation_criteria_plan_data(
    data: Optional[Dict[str, str]],
    uow: UnitOfWork = Provide[BackendContainer.uow],
    robot_service: RobotService = Provide[BackendContainer.backbone_container.robot_service],
    app_evaluation_criteria_plan_service: AppEvaluationCriteriaPlanService = Provide[
        BackendContainer.app_evaluation_criteria_plan_service
    ],
    redis_service: RedisService = Provide[BackendContainer.redis_service],
):
    """
    同步后更新计划相关的评价分配、分数录入日志等
    :param data:
    :param uow:
    :param robot_service:
    :param app_evaluation_criteria_plan_service:
    :param redis_service:
    :return:
    """
    try:
        key = EnumRedisFlag.FLAG_REFRESH_EVALUATION_CRITERIA_PLAN_DATA.name
        while redis_service.exists(key):
            time.sleep(10)
        with uow:
            redis_service.set(key=key, value=generate_by_host_and_time(), ex=30 * 60)
            handler = robot_service.get_system_robot().to_basic_handler()
            transaction = uow.log_transaction(
                handler=handler,
                action="task_refresh_evaluation_criteria_plan_data",
            )
            app_evaluation_criteria_plan_service.refresh_evaluation_criteria_plan_data(
                transaction=transaction
            )
        redis_service.delete(key=key)
    except Exception as error:
        logging.error(error)
        traceback.print_exc()


@inject
def task_save_evaluation_assignment_relationship(
    data: Dict[str, str],
    uow: UnitOfWork = Provide[BackendContainer.uow],
    robot_service: RobotService = Provide[BackendContainer.backbone_container.robot_service],
    app_evaluation_assignment_service: AppEvaluationAssignmentService = Provide[
        BackendContainer.app_evaluation_assignment_service
    ],
    redis_service: RedisService = Provide[BackendContainer.redis_service],
):
    """
    保存评价分配关系
    :param data:
    :param uow:
    :param robot_service:
    :param app_evaluation_assignment_service:
    :param redis_service:
    :return:
    """

    try:
        key = EnumRedisFlag.FLAG_SAVE_EVALUATION_ASSIGNMENT_RELATIONSHIP.name
        while redis_service.exists(key):
            time.sleep(10)
        with uow:
            params = SaveEvaluationAssignmentRelationshipModel(**data)
            redis_service.set(key=key, value=params.evaluation_criteria_plan.id, ex=30 * 60)
            handler = robot_service.get_system_robot().to_basic_handler()
            transaction = uow.log_transaction(
                handler=handler,
                action="task_save_evaluation_assignment_relationship",
                action_params={"data": data},
            )

            app_evaluation_assignment_service.save_evaluation_assignment_relationship(
                evaluation_criteria_plan=params.evaluation_criteria_plan,
                evaluation_criteria_plan_scope_list=params.evaluation_criteria_plan_scope_list,
                transaction=transaction
            )
        redis_service.delete(key=key)

    except Exception as error:
        logging.error(error)
        traceback.print_exc()


@inject
def task_disable_unavailable_user(
    data: Dict[str, str],
    uow: UnitOfWork = Provide[BackendContainer.uow],
    robot_service: RobotService = Provide[BackendContainer.backbone_container.robot_service],
    app_user_service: AppUserService = Provide[
        BackendContainer.app_user_service
    ],
):
    """
    禁用不可用的用户
    :param data:
    :param uow:
    :param robot_service:
    :param app_user_service:
    :return:
    """

    try:
        with uow:
            handler = robot_service.get_system_robot().to_basic_handler()
            transaction = uow.log_transaction(
                handler=handler,
                action="task_disable_unavailable_user",
                action_params={"data": data},
            )
            app_user_service.disable_unavailable_user(
                transaction=transaction
            )

    except Exception as error:
        logging.error(error)
        traceback.print_exc()


@inject
def task_sync_k12_teacher_subject(
    data: Optional[Dict[str, str]],
    uow: UnitOfWork = Provide[BackendContainer.uow],
    robot_service: RobotService = Provide[BackendContainer.backbone_container.robot_service],
    k12_teacher_subject_service: K12TeacherSubjectService = Provide[BackendContainer.edu_evaluation_container.k12_teacher_subject_service],
):
    """
    同步老师教授学科，因为有些老师已经离开班级
    :param data:
    :param uow:
    :param robot_service:
    :param k12_teacher_subject_service:
    :return:
    """

    try:
        with uow:
            handler = robot_service.get_system_robot().to_basic_handler()
            transaction = uow.log_transaction(
                handler=handler,
                action="task_sync_k12_teacher_subject",
            )
            k12_teacher_subject_service.sync_k12_teacher_subject(
                transaction=transaction
            )

    except Exception as error:
        logging.error(error)
        traceback.print_exc()
