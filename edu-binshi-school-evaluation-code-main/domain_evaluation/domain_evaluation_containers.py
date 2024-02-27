from dependency_injector import containers, providers
from infra_basic.sqlalchemy_uow import SqlAlchemyUnitOfWork

from domain_evaluation.repository.benchmark_execute_node_repository import (
    BenchmarkExecuteNodeRepository,
)
from domain_evaluation.repository.benchmark_input_node_repository import BenchmarkInputNodeRepository
from domain_evaluation.repository.benchmark_node_assistant_repository import (
    BenchmarkNodeAssistantRepository,
)
from domain_evaluation.repository.benchmark_repository import BenchmarkRepository
from domain_evaluation.repository.benchmark_score_repository import BenchmarkScoreRepository
from domain_evaluation.repository.benchmark_strategy_repository import BenchmarkStrategyRepository
from domain_evaluation.repository.calc_score_input_repository import CalcScoreInputRepository
from domain_evaluation.repository.calc_score_log_repository import CalcScoreLogRepository
from domain_evaluation.repository.calc_score_output_repository import CalcScoreOutputRepository
from domain_evaluation.repository.evaluation_assignment_repository import (
    EvaluationAssignmentRepository,
)
from domain_evaluation.repository.evaluation_criteria_plan_repository import (
    EvaluationCriteriaPlanRepository,
)
from domain_evaluation.repository.evaluation_criteria_plan_scope_repository import (
    EvaluationCriteriaPlanScopeRepository,
)
from domain_evaluation.repository.evaluation_criteria_repository import EvaluationCriteriaRepository
from domain_evaluation.repository.evaluation_criteria_tree_repository import (
    EvaluationCriteriaTreeRepository,
)
from domain_evaluation.repository.indicator_repository import IndicatorRepository
from domain_evaluation.repository.input_score_log_repository import InputScoreLogRepository
from domain_evaluation.repository.score_symbol_repository import ScoreSymbolRepository
from domain_evaluation.repository.todo_task_repository import TodoTaskRepository
from domain_evaluation.service.benchmark_execute_node_service import BenchmarkExecuteNodeService
from domain_evaluation.service.benchmark_manage_service import BenchmarkManageService
from domain_evaluation.service.benchmark_score_service import BenchmarkScoreService
from domain_evaluation.service.benchmark_service import BenchmarkService
from domain_evaluation.service.benchmark_strategy_factory import BenchmarkStrategyFactory
from domain_evaluation.service.benchmark_strategy_service import BenchmarkStrategyService
from domain_evaluation.service.calc_score_log_service import CalcScoreLogService
from domain_evaluation.service.evaluation_assignment_service import EvaluationAssignmentService
from domain_evaluation.service.evaluation_criteria_plan_scope_service import (
    EvaluationCriteriaPlanScopeService,
)
from domain_evaluation.service.evaluation_criteria_plan_service import EvaluationCriteriaPlanService
from domain_evaluation.service.evaluation_criteria_service import EvaluationCriteriaService
from domain_evaluation.service.evaluation_criteria_tree_service import EvaluationCriteriaTreeService
from domain_evaluation.service.evaluation_record_service import EvaluationRecordService
from domain_evaluation.service.indicator_service import IndicatorService
from domain_evaluation.service.input_score_log_service import InputScoreLogService
from domain_evaluation.service.node_calc_method_service import NodeCalcMethodService
from domain_evaluation.service.score_symbol_service import ScoreSymbolService
from domain_evaluation.service.todo_task_service import TodoTaskService
from edu_binshi.edu_evaluation_containers import EduEvaluationContainer
from infra_backbone.backbone_container import BackboneContainer
from infra_backbone.object_storage_container import ObjectStorageContainer


class DomainEvaluationContainer(containers.DeclarativeContainer):
    uow = providers.Dependency(instance_of=SqlAlchemyUnitOfWork)  # type: ignore

    backbone_container: BackboneContainer = providers.Container(
        BackboneContainer, uow=uow
    )  # type: ignore

    object_storage_container: ObjectStorageContainer = providers.Container(
        ObjectStorageContainer, uow=uow
    )  # type: ignore

    edu_evaluation_container: EduEvaluationContainer = providers.Container(
        EduEvaluationContainer, uow=uow
    )  # type: ignore

    evaluation_criteria_repository = providers.ThreadLocalSingleton(
        EvaluationCriteriaRepository, db_session=uow.provided.db_session
    )  # type: ignore

    evaluation_criteria_tree_repository = providers.ThreadLocalSingleton(
        EvaluationCriteriaTreeRepository, db_session=uow.provided.db_session
    )  # type: ignore

    indicator_repository = providers.ThreadLocalSingleton(
        IndicatorRepository, db_session=uow.provided.db_session
    )  # type: ignore

    benchmark_repository = providers.ThreadLocalSingleton(
        BenchmarkRepository, db_session=uow.provided.db_session
    )  # type: ignore

    score_symbol_repository = providers.ThreadLocalSingleton(
        ScoreSymbolRepository, db_session=uow.provided.db_session
    )  # type: ignore

    benchmark_execute_node_repository = providers.ThreadLocalSingleton(
        BenchmarkExecuteNodeRepository, db_session=uow.provided.db_session
    )  # type: ignore

    evaluation_criteria_plan_repository = providers.ThreadLocalSingleton(
        EvaluationCriteriaPlanRepository, db_session=uow.provided.db_session
    )  # type: ignore

    input_score_log_repository = providers.ThreadLocalSingleton(
        InputScoreLogRepository, db_session=uow.provided.db_session
    )  # type: ignore

    evaluation_assignment_repository = providers.ThreadLocalSingleton(
        EvaluationAssignmentRepository, db_session=uow.provided.db_session
    )  # type: ignore

    evaluation_criteria_plan_scope_repository = providers.ThreadLocalSingleton(
        EvaluationCriteriaPlanScopeRepository, db_session=uow.provided.db_session
    )  # type: ignore

    calc_score_log_repository = providers.ThreadLocalSingleton(
        CalcScoreLogRepository, db_session=uow.provided.db_session
    )  # type: ignore

    benchmark_score_repository = providers.ThreadLocalSingleton(
        BenchmarkScoreRepository, db_session=uow.provided.db_session
    )  # type: ignore

    calc_score_input_repository = providers.ThreadLocalSingleton(
        CalcScoreInputRepository, db_session=uow.provided.db_session
    )  # type: ignore

    calc_score_output_repository = providers.ThreadLocalSingleton(
        CalcScoreOutputRepository, db_session=uow.provided.db_session
    )  # type: ignore

    benchmark_node_assistant_repository = providers.ThreadLocalSingleton(
        BenchmarkNodeAssistantRepository, db_session=uow.provided.db_session
    )  # type: ignore

    benchmark_strategy_repository = providers.ThreadLocalSingleton(
        BenchmarkStrategyRepository, db_session=uow.provided.db_session
    )  # type: ignore

    benchmark_input_node_repository = providers.ThreadLocalSingleton(
        BenchmarkInputNodeRepository, db_session=uow.provided.db_session
    )  # type: ignore

    todo_task_repository = providers.ThreadLocalSingleton(
        TodoTaskRepository, db_session=uow.provided.db_session
    )  # type: ignore

    indicator_service = providers.ThreadLocalSingleton(
        IndicatorService,
        indicator_repository=indicator_repository,
    )  # type: ignore

    benchmark_execute_node_service = providers.ThreadLocalSingleton(
        BenchmarkExecuteNodeService,
        benchmark_execute_node_repository=benchmark_execute_node_repository,
    )

    benchmark_manage_service = providers.ThreadLocalSingleton(
        BenchmarkManageService,
        execute_node_service=benchmark_execute_node_service,
        subject_repository=edu_evaluation_container.subject_repository,
        benchmark_node_assistant_repository=benchmark_node_assistant_repository,
        team_category_repository=backbone_container.team_category_repository,
    )  # type: ignore

    benchmark_strategy_factory = providers.ThreadLocalSingleton(
        BenchmarkStrategyFactory,
        subject_repository=edu_evaluation_container.subject_repository,
        score_symbol_repository=score_symbol_repository,
        team_category_repository=backbone_container.team_category_repository,
        benchmark_repository=benchmark_repository,
    )  # type: ignore

    benchmark_strategy_service = providers.ThreadLocalSingleton(
        BenchmarkStrategyService,
        benchmark_strategy_factory=benchmark_strategy_factory,
        benchmark_strategy_repository=benchmark_strategy_repository,
        benchmark_repository=benchmark_repository,
    )  # type: ignore

    evaluation_criteria_service = providers.ThreadLocalSingleton(
        EvaluationCriteriaService,
        evaluation_criteria_repository=evaluation_criteria_repository,
        evaluation_criteria_plan_repository=evaluation_criteria_plan_repository,
    )  # type: ignore

    benchmark_service = providers.ThreadLocalSingleton(
        BenchmarkService,
        benchmark_repository=benchmark_repository,
        benchmark_manage_service=benchmark_manage_service,
        benchmark_strategy_service=benchmark_strategy_service,
        benchmark_execute_node_service=benchmark_execute_node_service,
        tag_service=backbone_container.tag_service,
        evaluation_criteria_service=evaluation_criteria_service,
    )  # type: ignore

    evaluation_criteria_tree_service = providers.ThreadLocalSingleton(
        EvaluationCriteriaTreeService,
        evaluation_criteria_tree_repository=evaluation_criteria_tree_repository,
        indicator_service=indicator_service,
        evaluation_criteria_service=evaluation_criteria_service,
        indicator_repository=indicator_repository,
        tag_repository=backbone_container.tag_repository,
        tag_service=backbone_container.tag_service,
        benchmark_service=benchmark_service,
    )  # type: ignore

    evaluation_criteria_plan_scope_service = providers.ThreadLocalSingleton(
        EvaluationCriteriaPlanScopeService,
        evaluation_criteria_plan_scope_repository=evaluation_criteria_plan_scope_repository,
        evaluation_criteria_plan_repository=evaluation_criteria_plan_repository,
    )  # type: ignore

    evaluation_criteria_plan_service = providers.ThreadLocalSingleton(
        EvaluationCriteriaPlanService,
        evaluation_criteria_plan_repository=evaluation_criteria_plan_repository,
        input_score_log_repository=input_score_log_repository,
    )  # type: ignore

    todo_task_service = providers.ThreadLocalSingleton(
        TodoTaskService,
        todo_task_repository=todo_task_repository,
        site_message_service=backbone_container.site_message_service,
        evaluation_criteria_plan_repository=evaluation_criteria_plan_repository,
        user_repository=backbone_container.user_repository,
    )  # type: ignore

    input_score_log_service = providers.ThreadLocalSingleton(
        InputScoreLogService,
        input_score_log_repository=input_score_log_repository,
        benchmark_manage_service=benchmark_manage_service,
        benchmark_execute_node_repository=benchmark_execute_node_repository,
        benchmark_input_node_repository=benchmark_input_node_repository,
        evaluation_criteria_plan_repository=evaluation_criteria_plan_repository,
        evaluation_assignment_repository=evaluation_assignment_repository,
        todo_task_service=todo_task_service,
        role_repository=backbone_container.role_repository,
    )  # type: ignore

    evaluation_assignment_service = providers.ThreadLocalSingleton(
        EvaluationAssignmentService,
        evaluation_assignment_repository=evaluation_assignment_repository,
        object_storage_service=object_storage_container.object_storage_service,
    )  # type: ignore

    score_symbol_service = providers.ThreadLocalSingleton(
        ScoreSymbolService,
        score_symbol_repository=score_symbol_repository,
    )  # type: ignore

    evaluation_record_service = providers.ThreadLocalSingleton(
        EvaluationRecordService,
        evaluation_criteria_tree_repository=evaluation_criteria_tree_repository,
        benchmark_input_node_repository=benchmark_input_node_repository,
    )  # type: ignore

    node_calc_method_service = providers.ThreadLocalSingleton(
        NodeCalcMethodService,
        benchmark_execute_node_repository=benchmark_execute_node_repository,
    )  # type: ignore

    calc_score_log_service = providers.ThreadLocalSingleton(
        CalcScoreLogService,
        calc_score_log_repository=calc_score_log_repository,
        evaluation_criteria_repository=evaluation_criteria_repository,
        evaluation_criteria_plan_repository=evaluation_criteria_plan_repository,
        evaluation_assignment_repository=evaluation_assignment_repository,
        benchmark_execute_node_repository=benchmark_execute_node_repository,
    )  # type: ignore

    benchmark_score_service = providers.ThreadLocalSingleton(
        BenchmarkScoreService,
        benchmark_repository=benchmark_repository,
        benchmark_score_repository=benchmark_score_repository,
        calc_score_input_repository=calc_score_input_repository,
        calc_score_output_repository=calc_score_output_repository,
        node_calc_method_service=node_calc_method_service,
    )  # type: ignore

