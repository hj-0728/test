from dependency_injector import containers, providers
from infra_basic.sqlalchemy_uow import SqlAlchemyUnitOfWork

from context_sync.repository.context_dept_map_repository import ContextDeptMapRepository
from context_sync.repository.context_organization_corp_map_repository import (
    ContextOrganizationCorpMapRepository,
)
from context_sync.repository.context_people_user_map_repository import (
    ContextPeopleUserMapRepository,
)
from context_sync.repository.context_sync_log_repository import ContextSyncLogRepository
from context_sync.service.sync_dingtalk_dept_service import SyncDingtalkDeptService
from context_sync.service.sync_dingtalk_service import SyncDingtalkService
from context_sync.service.sync_dingtalk_user_service import SyncDingtalkUserService
from infra_backbone.backbone_container import BackboneContainer
from infra_backbone.object_storage_container import ObjectStorageContainer
from infra_dingtalk.dingtalk_container import DingtalkContainer


class ContextSyncContainer(containers.DeclarativeContainer):
    uow = providers.Dependency(instance_of=SqlAlchemyUnitOfWork)  # type: ignore

    backbone_container: BackboneContainer = providers.Container(
        BackboneContainer, uow=uow
    )  # type: ignore

    object_storage_container: ObjectStorageContainer = providers.Container(
        ObjectStorageContainer, uow=uow
    )  # type: ignore

    dingtalk_container: DingtalkContainer = providers.Container(
        DingtalkContainer, uow=uow
    )  # type: ignore

    context_dept_map_repository = providers.ThreadLocalSingleton(
        ContextDeptMapRepository, db_session=uow.provided.db_session
    )  # type: ignore

    context_people_user_map_repository = providers.ThreadLocalSingleton(
        ContextPeopleUserMapRepository, db_session=uow.provided.db_session
    )  # type: ignore

    context_org_corp_map_repository = providers.ThreadLocalSingleton(
        ContextOrganizationCorpMapRepository, db_session=uow.provided.db_session
    )  # type: ignore

    context_sync_log_repository = providers.ThreadLocalSingleton(
        ContextSyncLogRepository, db_session=uow.provided.db_session
    )  # type: ignore

    sync_dingtalk_dept_service = providers.ThreadLocalSingleton(
        SyncDingtalkDeptService,
        dingtalk_k12_dept_repository=dingtalk_container.dingtalk_k12_dept_repository,
        context_dept_map_repository=context_dept_map_repository,
        dept_service=backbone_container.dept_service,
        dept_dept_category_map_service=backbone_container.dept_dept_category_map_service,
        dimension_dept_tree_repository=backbone_container.dimension_dept_tree_repository,
        dingtalk_dept_repository=dingtalk_container.dingtalk_dept_repository,
    )  # type: ignore

    sync_dingtalk_user_service = providers.ThreadLocalSingleton(
        SyncDingtalkUserService,
        context_people_user_map_repository=context_people_user_map_repository,
        dingtalk_k12_parent_repository=dingtalk_container.dingtalk_k12_parent_repository,
        dingtalk_k12_student_repository=dingtalk_container.dingtalk_k12_student_repository,
        dingtalk_user_repository=dingtalk_container.dingtalk_user_repository,
        people_service=backbone_container.people_service,
        object_storage_service=object_storage_container.object_storage_service,
        contact_info_service=backbone_container.contact_info_service,
    )  # type: ignore

    sync_dingtalk_service = providers.ThreadLocalSingleton(
        SyncDingtalkService,
        sync_dingtalk_dept_service=sync_dingtalk_dept_service,
        sync_dingtalk_user_service=sync_dingtalk_user_service,
        context_org_corp_map_repository=context_org_corp_map_repository,
        context_dept_map_repository=context_dept_map_repository,
    )  # type: ignore
