from dependency_injector import containers, providers
from infra_basic.redis_manager import RedisManager
from infra_basic.sqlalchemy_uow import SqlAlchemyUnitOfWork

from biz_comprehensive.repository.calc_log_repository import CalcLogRepository
from biz_comprehensive.repository.calc_rule_pre_depends_repository import (
    CalcRulePreDependsRepository,
)
from biz_comprehensive.repository.calc_rule_repository import CalcRuleRepository
from biz_comprehensive.repository.calc_trigger_repository import CalcTriggerRepository
from biz_comprehensive.repository.causation_repository import CausationRepository
from biz_comprehensive.repository.class_report_repository import ClassReportRepository
from biz_comprehensive.repository.indicator_final_score_repository import (
    IndicatorFinalScoreRepository,
)
from biz_comprehensive.repository.indicator_score_log_repository import IndicatorScoreLogRepository
from biz_comprehensive.repository.log_clue_repository import LogClueRepository
from biz_comprehensive.repository.medal_issued_log_repository import MedalIssuedLogRepository
from biz_comprehensive.repository.observation_action_repository import ObservationActionRepository
from biz_comprehensive.repository.observation_point_log_repository import (
    ObservationPointLogRepository,
)
from biz_comprehensive.repository.observation_point_points_snapshot_repository import (
    ObservationPointPointsSnapshotRepository,
)
from biz_comprehensive.repository.observation_point_repository import ObservationPointRepository
from biz_comprehensive.repository.parent_repository import ParentRepository
from biz_comprehensive.repository.period_category_repository import PeriodCategoryRepository
from biz_comprehensive.repository.period_repository import PeriodRepository
from biz_comprehensive.repository.points_log_repository import PointsLogRepository
from biz_comprehensive.repository.scene_obeservation_point_assign_repository import (
    SceneObservationPointAssignRepository,
)
from biz_comprehensive.repository.scene_repository import SceneRepository
from biz_comprehensive.repository.scene_terminal_assign_repository import (
    SceneTerminalAssignRepository,
)
from biz_comprehensive.repository.search_history_repository import SearchHistoryRepository
from biz_comprehensive.repository.student_points_log_repository import StudentPointsLogRepository
from biz_comprehensive.repository.student_report_repository import StudentReportRepository
from biz_comprehensive.repository.symbol_repository import SymbolRepository
from biz_comprehensive.repository.teacher_repository import TeacherRepository
from biz_comprehensive.service.calc_resource_service import CalcResourceService
from biz_comprehensive.service.calc_rule_calc_func_service import CalcRuleCalcFuncService
from biz_comprehensive.service.calc_rule_post_func_service import CalcRulePostFuncService
from biz_comprehensive.service.calc_rule_pre_func_service import CalcRulePreFuncService
from biz_comprehensive.service.calc_rule_service import CalcRuleService
from biz_comprehensive.service.calc_service import CalcService
from biz_comprehensive.service.calc_trigger_service import CalcTriggerService
from biz_comprehensive.service.class_report_service import ClassReportService
from biz_comprehensive.service.indicator_score_service import IndicatorScoreService
from biz_comprehensive.service.medal_issued_log_service import MedalIssuedLogService
from biz_comprehensive.service.observation_action_service import ObservationActionService
from biz_comprehensive.service.observation_point_log_service import ObservationPointLogService
from biz_comprehensive.service.observation_point_points_snapshot_service import (
    ObservationPointPointsSnapshotService,
)
from biz_comprehensive.service.observation_point_service import ObservationPointService
from biz_comprehensive.service.parent_service import ParentService
from biz_comprehensive.service.period_service import PeriodService
from biz_comprehensive.service.points_log_service import PointsLogService
from biz_comprehensive.service.save_calc_result_service import SaveCalcResultService
from biz_comprehensive.service.scene_observation_point_assign_service import (
    SceneObservationPointAssignService,
)
from biz_comprehensive.service.scene_service import SceneService
from biz_comprehensive.service.scene_terminal_assign_servive import SceneTerminalAssignService
from biz_comprehensive.service.search_history_service import SearchHistoryService
from biz_comprehensive.service.snapshot_service import SnapshotService
from biz_comprehensive.service.student_points_log_service import StudentPointsLogService
from biz_comprehensive.service.student_report_service import StudentReportService
from biz_comprehensive.service.symbol_service import SymbolService
from biz_comprehensive.service.teacher_service import TeacherService
from infra_backbone.backbone_container import BackboneContainer
from infra_backbone.object_storage_container import ObjectStorageContainer


class ComprehensiveContainer(containers.DeclarativeContainer):
    uow = providers.Dependency(instance_of=SqlAlchemyUnitOfWork)
    redis_manager = providers.ThreadLocalSingleton(RedisManager)

    object_storage_container: ObjectStorageContainer = providers.Container(
        ObjectStorageContainer, uow=uow
    )  # type: ignore

    backbone_container: BackboneContainer = providers.Container(BackboneContainer, uow=uow)  # type: ignore

    scene_repository = providers.ThreadLocalSingleton(
        SceneRepository,
        db_session=uow.provided.db_session,
    )

    scene_terminal_assign_repository = providers.ThreadLocalSingleton(
        SceneTerminalAssignRepository,
        db_session=uow.provided.db_session,
    )

    scene_observation_point_assign_repository = providers.ThreadLocalSingleton(
        SceneObservationPointAssignRepository,
        db_session=uow.provided.db_session,
    )

    symbol_repository = providers.ThreadLocalSingleton(
        SymbolRepository,
        db_session=uow.provided.db_session,
    )

    observation_point_repository = providers.ThreadLocalSingleton(
        ObservationPointRepository, db_session=uow.provided.db_session
    )

    calc_trigger_repository = providers.ThreadLocalSingleton(
        CalcTriggerRepository, db_session=uow.provided.db_session
    )

    calc_rule_repository = providers.ThreadLocalSingleton(
        CalcRuleRepository, db_session=uow.provided.db_session
    )

    search_history_repository = providers.ThreadLocalSingleton(
        SearchHistoryRepository, db_session=uow.provided.db_session
    )

    student_points_log_repository = providers.ThreadLocalSingleton(
        StudentPointsLogRepository, db_session=uow.provided.db_session
    )

    points_log_repository = providers.ThreadLocalSingleton(
        PointsLogRepository, db_session=uow.provided.db_session
    )

    period_category_repository = providers.ThreadLocalSingleton(
        PeriodCategoryRepository, db_session=uow.provided.db_session
    )

    period_repository = providers.ThreadLocalSingleton(
        PeriodRepository, db_session=uow.provided.db_session
    )

    calc_rule_pre_depends_repository = providers.ThreadLocalSingleton(
        CalcRulePreDependsRepository, db_session=uow.provided.db_session
    )

    class_report_repository = providers.ThreadLocalSingleton(
        ClassReportRepository, db_session=uow.provided.db_session
    )

    calc_log_repository = providers.ThreadLocalSingleton(
        CalcLogRepository, db_session=uow.provided.db_session
    )

    causation_repository = providers.ThreadLocalSingleton(
        CausationRepository, db_session=uow.provided.db_session
    )

    indicator_final_score_repository = providers.ThreadLocalSingleton(
        IndicatorFinalScoreRepository, db_session=uow.provided.db_session
    )

    indicator_score_log_repository = providers.ThreadLocalSingleton(
        IndicatorScoreLogRepository, db_session=uow.provided.db_session
    )

    log_clue_repository = providers.ThreadLocalSingleton(
        LogClueRepository, db_session=uow.provided.db_session
    )

    medal_issued_log_repository = providers.ThreadLocalSingleton(
        MedalIssuedLogRepository, db_session=uow.provided.db_session
    )

    observation_point_log_repository = providers.ThreadLocalSingleton(
        ObservationPointLogRepository, db_session=uow.provided.db_session
    )

    observation_action_repository = providers.ThreadLocalSingleton(
        ObservationActionRepository, db_session=uow.provided.db_session
    )

    teacher_repository = providers.ThreadLocalSingleton(
        TeacherRepository, db_session=uow.provided.db_session
    )

    observation_point_points_snapshot_repository = providers.ThreadLocalSingleton(
        ObservationPointPointsSnapshotRepository, db_session=uow.provided.db_session
    )

    student_report_repository = providers.ThreadLocalSingleton(
        StudentReportRepository, db_session=uow.provided.db_session
    )

    parent_repository = providers.ThreadLocalSingleton(
        ParentRepository,
        db_session=uow.provided.db_session,
    )

    calc_trigger_service = providers.ThreadLocalSingleton(
        CalcTriggerService,
        calc_trigger_repository=calc_trigger_repository,
        calc_rule_repository=calc_rule_repository,
    )

    calc_rule_calc_func_service = providers.ThreadLocalSingleton(
        CalcRuleCalcFuncService,
    )

    calc_rule_post_func_service = providers.ThreadLocalSingleton(
        CalcRulePostFuncService,
    )

    calc_rule_pre_func_service = providers.ThreadLocalSingleton(
        CalcRulePreFuncService,
        calc_rule_pre_depends_repository=calc_rule_pre_depends_repository,
        establishment_assign_repository=backbone_container.establishment_assign_repository,
    )

    period_service = providers.ThreadLocalSingleton(
        PeriodService,
        period_repository=period_repository,
    )

    points_log_service = providers.ThreadLocalSingleton(
        PointsLogService,
        points_log_repository=points_log_repository,
        period_service=period_service,
    )

    medal_issued_log_service = providers.ThreadLocalSingleton(
        MedalIssuedLogService,
        medal_issued_log_repository=medal_issued_log_repository,
    )

    indicator_score_service = providers.ThreadLocalSingleton(
        IndicatorScoreService,
        indicator_score_log_repository=indicator_score_log_repository,
        indicator_final_score_repository=indicator_final_score_repository,
    )

    calc_rule_service = providers.ThreadLocalSingleton(
        CalcRuleService,
        calc_rule_repository=calc_rule_repository,
        calc_rule_pre_func_service=calc_rule_pre_func_service,
        calc_rule_calc_func_service=calc_rule_calc_func_service,
        calc_rule_post_func_service=calc_rule_post_func_service,
    )

    save_calc_result_service = providers.ThreadLocalSingleton(
        SaveCalcResultService,
        calc_log_repository=calc_log_repository,
        causation_repository=causation_repository,
        points_log_service=points_log_service,
        medal_issued_log_service=medal_issued_log_service,
        indicator_score_service=indicator_score_service,
        log_clue_repository=log_clue_repository,
    )

    calc_service = providers.ThreadLocalSingleton(
        CalcService,
        calc_trigger_service=calc_trigger_service,
        calc_rule_service=calc_rule_service,
        symbol_repository=symbol_repository,
        save_calc_result_service=save_calc_result_service,
    )

    scene_terminal_assign_service = providers.ThreadLocalSingleton(
        SceneTerminalAssignService,
        scene_terminal_assign_repository=scene_terminal_assign_repository,
    )

    scene_observation_point_assign_service = providers.ThreadLocalSingleton(
        SceneObservationPointAssignService,
        scene_observation_point_assign_repository=scene_observation_point_assign_repository,
    )

    observation_point_service = providers.ThreadLocalSingleton(
        ObservationPointService,
        observation_point_repository=observation_point_repository,
        object_storage_service=object_storage_container.object_storage_service,
        calc_service=calc_service,
        calc_trigger_service=calc_trigger_service,
        dict_repository=backbone_container.dict_repository,
        scene_observation_point_assign_service=scene_observation_point_assign_service,
        file_public_link_repository=backbone_container.file_public_link_repository,
    )

    scene_service = providers.ThreadLocalSingleton(
        SceneService,
        scene_repository=scene_repository,
        scene_terminal_assign_service=scene_terminal_assign_service,
        scene_observation_point_assign_service=scene_observation_point_assign_service,
    )

    search_history_service = providers.ThreadLocalSingleton(
        SearchHistoryService,
        search_history_repository=search_history_repository,
    )

    symbol_service = providers.ThreadLocalSingleton(
        SymbolService,
        symbol_repository=symbol_repository,
    )

    student_points_log_service = providers.ThreadLocalSingleton(
        StudentPointsLogService,
        student_points_log_repository=student_points_log_repository,
        symbol_repository=symbol_repository,
        symbol_service=symbol_service,
        dept_service=backbone_container.dept_service,
    )

    class_report_service = providers.ThreadLocalSingleton(
        ClassReportService,
        class_report_repository=class_report_repository,
        object_storage_service=object_storage_container.object_storage_service,
    )

    observation_point_log_service = providers.ThreadLocalSingleton(
        ObservationPointLogService,
        observation_point_log_repository=observation_point_log_repository,
        object_storage_service=object_storage_container.object_storage_service,
    )

    observation_action_service = providers.ThreadLocalSingleton(
        ObservationActionService,
        observation_action_repository=observation_action_repository,
        observation_point_log_service=observation_point_log_service,
    )

    teacher_service = providers.ThreadLocalSingleton(
        TeacherService,
        teacher_repository=teacher_repository,
        search_history_service=search_history_service,
    )

    calc_resource_service = providers.ThreadLocalSingleton(
        CalcResourceService,
        observation_point_log_service=observation_point_log_service,
    )

    observation_point_points_snapshot_service = providers.ThreadLocalSingleton(
        ObservationPointPointsSnapshotService,
        observation_point_points_snapshot_repository=observation_point_points_snapshot_repository,
    )

    snapshot_service = providers.ThreadLocalSingleton(
        SnapshotService,
        observation_point_points_snapshot_service=observation_point_points_snapshot_service,
    )

    student_report_service = providers.ThreadLocalSingleton(
        StudentReportService,
        student_report_repository=student_report_repository,
    )

    parent_service = providers.ThreadLocalSingleton(
        ParentService,
        parent_repository=parent_repository,
    )
