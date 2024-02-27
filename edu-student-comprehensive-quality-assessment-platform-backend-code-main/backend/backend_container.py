from dependency_injector import containers, providers
from infra_basic.database import Database
from infra_basic.redis_manager import RedisManager
from infra_basic.sqlalchemy_uow import SqlAlchemyUnitOfWork
from infra_pub_sub_manager.sync_pub_client import SyncPubClient

from backend.repository.auth_repository import AuthRepository
from backend.service.app_ability_permission_service import AppAbilityPermissionService
from backend.service.app_menu_service import AppMenuService
from backend.service.app_role_service import AppRoleService
from backend.service.auth_service import AuthService
from backend.service.redis_service import RedisService
from backend.service.tasks_service import TasksService
from biz_comprehensive.comprehensive_container import ComprehensiveContainer
from context_sync.context_sync_container import ContextSyncContainer
from infra_backbone.backbone_container import BackboneContainer
from infra_backbone.object_storage_container import ObjectStorageContainer
from infra_dingtalk.dingtalk_container import DingtalkContainer


class BackendContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "backend",
            "biz_comprehensive",
            "context_sync",
            "infra_backbone",
            "infra_dingtalk",
        ]
    )
    redis_manager = providers.ThreadLocalSingleton(RedisManager)
    database = providers.ThreadLocalSingleton(Database)
    pub_client = providers.ThreadLocalSingleton(SyncPubClient)
    uow = providers.ThreadLocalSingleton(SqlAlchemyUnitOfWork, engine=database.provided.engine)

    backbone_container: BackboneContainer = providers.Container(BackboneContainer, uow=uow)  # type: ignore

    comprehensive_container: ComprehensiveContainer = providers.Container(
        ComprehensiveContainer, uow=uow
    )

    dingtalk_container: DingtalkContainer = providers.Container(DingtalkContainer, uow=uow)

    context_sync_container: ContextSyncContainer = providers.Container(
        ContextSyncContainer, uow=uow
    )

    object_storage_container: ObjectStorageContainer = providers.Container(
        ObjectStorageContainer, uow=uow
    )  # type: ignore

    auth_repository = providers.ThreadLocalSingleton(
        AuthRepository, db_session=uow.provided.db_session
    )

    redis_service = providers.ThreadLocalSingleton(
        RedisService,
        user_repository=backbone_container.user_repository,
        role_service=backbone_container.role_service,
        redis_manager=redis_manager,
        period_service=comprehensive_container.period_service,
        robot_service=backbone_container.robot_service,
    )

    app_role_service = providers.ThreadLocalSingleton(
        AppRoleService,
        redis_manager=redis_manager,
        role_repository=backbone_container.role_repository,
        auth_repository=auth_repository,
        redis_service=redis_service,
    )  # type: ignore

    app_menu_service = providers.ThreadLocalSingleton(
        AppMenuService,
        menu_repository=backbone_container.menu_repository,
    )  # type: ignore

    app_ability_permission_service = providers.ThreadLocalSingleton(
        AppAbilityPermissionService,
        redis_manager=redis_manager,
        user_repository=backbone_container.user_repository,
        redis_service=redis_service,
    )  # type: ignore

    auth_service = providers.ThreadLocalSingleton(
        AuthService,
        auth_repository=auth_repository,
        redis_service=redis_service,
        dingtalk_auth_service=dingtalk_container.dingtalk_auth_service,
        context_people_user_map_service=context_sync_container.context_people_user_map_service,
        user_service=backbone_container.user_service,
        app_role_service=app_role_service,
        app_ability_permission_service=app_ability_permission_service,
    )

    tasks_service = providers.ThreadLocalSingleton(
        TasksService,
        calc_service=comprehensive_container.calc_service,
        calc_resource_service=comprehensive_container.calc_resource_service,
        distributed_task_log_service=backbone_container.distributed_task_log_service,
        snapshot_service=comprehensive_container.snapshot_service,
        points_log_service=comprehensive_container.points_log_service,
    )
