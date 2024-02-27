from dependency_injector import containers, providers
from infra_basic.database import Database
from infra_basic.redis_manager import RedisManager
from infra_basic.sqlalchemy_uow import SqlAlchemyUnitOfWork
from infra_pub_sub_manager.sync_pub_client import SyncPubClient

from backend.repository.app_establishment_assignment_repository import (
    AppEstablishmentAssignmentRepository,
)
from backend.repository.app_evaluation_criteria_plan_repository import (
    AppEvaluationCriteriaPlanRepository,
)
from backend.repository.app_input_score_log_repository import AppInputScoreLogRepository
from backend.repository.evaluation_criteria_plan_statistics_repository import (
    EvaluationCriteriaPlanStatisticsRepository,
)
from backend.repository.storage_repository import StorageRepository
from backend.service.app_ability_permission_service import AppAbilityPermissionService
from backend.service.app_dingtalk_user_service import AppDingtalkUserService
from backend.service.app_evaluation_assignment_service import AppEvaluationAssignmentService
from backend.service.app_evaluation_criteria_plan_scope_service import (
    AppEvaluationCriteriaPlanScopeService,
)
from backend.service.app_evaluation_criteria_plan_service import AppEvaluationCriteriaPlanService
from backend.service.app_input_score_log_service import AppInputScoreLogService
from backend.service.app_role_service import AppRoleService
from backend.service.app_student_service import AppStudentService
from backend.service.app_team_service import AppTeamService
from backend.service.app_user_service import AppUserService
from backend.service.authorization_service import AuthorizationService
from backend.service.evaluation_criteria_plan_statistics_service import (
    EvaluationCriteriaPlanStatisticsService,
)
from backend.service.evaluation_report_service import EvaluationReportService
from backend.service.period_service import PeriodService
from backend.service.redis_service import RedisService
from context_sync.context_sync_containers import ContextSyncContainer
from domain_evaluation.domain_evaluation_containers import DomainEvaluationContainer
from edu_binshi.edu_evaluation_containers import EduEvaluationContainer
from infra_backbone.backbone_container import BackboneContainer
from infra_backbone.object_storage_container import ObjectStorageContainer
from infra_dingtalk.dingtalk_container import DingtalkContainer
from backend.service.storage_service import StorageService


class BackendContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["backend"])

    redis_manager = providers.ThreadLocalSingleton(RedisManager)  # type: ignore

    database = providers.ThreadLocalSingleton(Database)  # type: ignore

    pub_client = providers.ThreadLocalSingleton(SyncPubClient)  # type: ignore

    uow = providers.ThreadLocalSingleton(SqlAlchemyUnitOfWork, engine=database.provided.engine)  # type: ignore

    dingtalk_container: DingtalkContainer = providers.Container(DingtalkContainer, uow=uow)

    backbone_container: BackboneContainer = providers.Container(BackboneContainer, uow=uow)  # type: ignore

    edu_evaluation_container: EduEvaluationContainer = providers.Container(EduEvaluationContainer, uow=uow)  # type: ignore

    context_sync_containers: ContextSyncContainer = providers.Container(ContextSyncContainer, uow=uow)  # type: ignore

    domain_evaluation_container: DomainEvaluationContainer = providers.Container(DomainEvaluationContainer, uow=uow)  # type: ignore

    object_storage_container: ObjectStorageContainer = providers.Container(
        ObjectStorageContainer, uow=uow
    )  # type: ignore

    storage_repository = providers.ThreadLocalSingleton(
        StorageRepository, db_session=uow.provided.db_session
    )

    app_establishment_assignment_repository = providers.ThreadLocalSingleton(
        AppEstablishmentAssignmentRepository, db_session=uow.provided.db_session
    )

    app_evaluation_criteria_plan_repository = providers.ThreadLocalSingleton(
        AppEvaluationCriteriaPlanRepository, db_session=uow.provided.db_session
    )

    evaluation_criteria_plan_statistics_repository = providers.ThreadLocalSingleton(
        EvaluationCriteriaPlanStatisticsRepository, db_session=uow.provided.db_session
    )

    app_input_score_log_repository = providers.ThreadLocalSingleton(
        AppInputScoreLogRepository, db_session=uow.provided.db_session
    )

    redis_service = providers.ThreadLocalSingleton(
        RedisService,
        user_repository=backbone_container.user_repository,
        role_service=backbone_container.role_service,
        redis_manager=redis_manager,
        dingtalk_k12_parent_repository=dingtalk_container.dingtalk_k12_parent_repository,
        dingtalk_user_repository=dingtalk_container.dingtalk_user_repository,
    )  # type: ignore

    authorization_service = providers.ThreadLocalSingleton(
        AuthorizationService,
        route_service=backbone_container.route_service,
        redis_service=redis_service,
        dingtalk_corp_repository=dingtalk_container.dingtalk_corp_repository,
        dingtalk_auth_service=dingtalk_container.auth_service,
        dingtalk_user_repository=dingtalk_container.dingtalk_user_repository,
        dingtalk_k12_parent_repository=dingtalk_container.dingtalk_k12_parent_repository,
        capacity_repository=backbone_container.capacity_repository,
    )  # type: ignore

    app_evaluation_assignment_service = providers.ThreadLocalSingleton(
        AppEvaluationAssignmentService,
        evaluation_assignment_service=domain_evaluation_container.evaluation_assignment_service,
        app_establishment_assignment_repository=app_establishment_assignment_repository,
        benchmark_execute_node_repository=domain_evaluation_container.benchmark_execute_node_repository,
        input_score_log_service=domain_evaluation_container.input_score_log_service,
        calc_score_log_service=domain_evaluation_container.calc_score_log_service,
        evaluation_criteria_repository=domain_evaluation_container.evaluation_criteria_repository,
        evaluation_assignment_repository=domain_evaluation_container.evaluation_assignment_repository,
    )  # type: ignore

    app_user_service = providers.ThreadLocalSingleton(
        AppUserService,
        user_service=backbone_container.user_service,
        user_repository=backbone_container.user_repository,
        redis_service=redis_service,
        role_service=backbone_container.role_service,
        authorization_service=authorization_service,
        redis_manager=redis_manager,
        student_service=edu_evaluation_container.student_service,
    )  # type: ignore

    app_role_service = providers.ThreadLocalSingleton(
        AppRoleService,
        redis_manager=redis_manager,
        role_repository=backbone_container.role_repository,
    )  # type: ignore

    app_ability_permission_service = providers.ThreadLocalSingleton(
        AppAbilityPermissionService,
        redis_manager=redis_manager,
    )  # type: ignore

    app_dingtalk_user_service = providers.ThreadLocalSingleton(
        AppDingtalkUserService,
        redis_manager=redis_manager,
        dingtalk_user_repository=dingtalk_container.dingtalk_user_repository,
        dingtalk_parent_repository=dingtalk_container.dingtalk_k12_parent_repository,
        capacity_repository=backbone_container.capacity_repository,
    )  # type: ignore

    period_service = providers.ThreadLocalSingleton(
        PeriodService,
        period_repository=edu_evaluation_container.period_repository,
        redis_manager=redis_manager,
        redis_service=redis_service,
    )

    app_evaluation_criteria_plan_scope_service = providers.ThreadLocalSingleton(
        AppEvaluationCriteriaPlanScopeService,
        evaluation_criteria_plan_scope_service=domain_evaluation_container.evaluation_criteria_plan_scope_service,
        app_evaluation_assignment_service=app_evaluation_assignment_service,
        evaluation_criteria_plan_repository=domain_evaluation_container.evaluation_criteria_plan_repository,
        evaluation_criteria_plan_scope_repository=domain_evaluation_container.evaluation_criteria_plan_scope_repository,
        dept_repository=backbone_container.dept_repository,
        establishment_assign_repository=backbone_container.establishment_assign_repository,
    )

    app_student_service = providers.ThreadLocalSingleton(
        AppStudentService,
        student_service=edu_evaluation_container.student_service,
        object_storage_service=object_storage_container.object_storage_service,
    )  # type: ignore

    evaluation_criteria_plan_statistics_service = providers.ThreadLocalSingleton(
        EvaluationCriteriaPlanStatisticsService,
        evaluation_criteria_plan_statistics_repository=evaluation_criteria_plan_statistics_repository,
        dimension_service=backbone_container.dimension_service,
        benchmark_repository=domain_evaluation_container.benchmark_repository,
        object_storage_service=object_storage_container.object_storage_service,
        evaluation_criteria_plan_service=domain_evaluation_container.evaluation_criteria_plan_service,
        organization_service=backbone_container.organization_service,
    )  # type: ignore

    app_input_score_log_service = providers.ThreadLocalSingleton(
        AppInputScoreLogService,
        input_score_log_repository=domain_evaluation_container.input_score_log_repository,
        input_score_log_service=domain_evaluation_container.input_score_log_service,
        team_member_repository=backbone_container.team_member_repository,
        benchmark_repository=domain_evaluation_container.benchmark_repository,
        app_input_score_log_repository=app_input_score_log_repository,
        benchmark_manage_service=domain_evaluation_container.benchmark_manage_service,
    )  # type: ignore

    app_team_service = providers.ThreadLocalSingleton(
        AppTeamService,
        team_service=backbone_container.team_service,
        app_evaluation_criteria_plan_repository=app_evaluation_criteria_plan_repository,
    )  # type: ignore

    app_evaluation_criteria_plan_service = providers.ThreadLocalSingleton(
        AppEvaluationCriteriaPlanService,
        evaluation_criteria_plan_service=domain_evaluation_container.evaluation_criteria_plan_service,
        app_evaluation_criteria_plan_scope_service=app_evaluation_criteria_plan_scope_service,
        evaluation_criteria_plan_repository=domain_evaluation_container.evaluation_criteria_plan_repository,
        app_evaluation_assignment_service=app_evaluation_assignment_service,
    )  # type: ignore

    evaluation_report_service = providers.ThreadLocalSingleton(
        EvaluationReportService,
        report_repository=edu_evaluation_container.report_repository,
        evaluation_criteria_plan_service=domain_evaluation_container.evaluation_criteria_plan_service,
        organization_service=backbone_container.organization_service,
    )
    storage_service = providers.ThreadLocalSingleton(
        StorageService, object_storage_service=object_storage_container.object_storage_service
    )