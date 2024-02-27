from dependency_injector import containers, providers
from infra_basic.redis_manager import RedisManager
from infra_basic.sqlalchemy_uow import SqlAlchemyUnitOfWork

from infra_dingtalk.repository.dingtalk_agent_repository import DingtalkAgentRepository
from infra_dingtalk.repository.dingtalk_corp_repository import DingtalkCorpRepository
from infra_dingtalk.repository.dingtalk_dept_repository import DingtalkDeptRepository
from infra_dingtalk.repository.dingtalk_dept_user_duty_repository import (
    DingtalkDeptUserDutyRepository,
)
from infra_dingtalk.repository.dingtalk_k12_dept_repository import DingtalkK12DeptRepository
from infra_dingtalk.repository.dingtalk_k12_dept_student_repository import (
    DingtalkK12DeptStudentRepository,
)
from infra_dingtalk.repository.dingtalk_k12_family_relationship_repository import (
    DingtalkK12FamilyRelationshipRepository,
)
from infra_dingtalk.repository.dingtalk_k12_parent_repository import DingtalkK12ParentRepository
from infra_dingtalk.repository.dingtalk_k12_student_repository import DingtalkK12StudentRepository
from infra_dingtalk.repository.dingtalk_sync_log_repository import DingtalkSyncLogRepository
from infra_dingtalk.repository.dingtalk_user_k12_dept_duty_repository import (
    DingtalkUserK12DeptDutyRepository,
)
from infra_dingtalk.repository.dingtalk_user_repository import DingtalkUserRepository
from infra_dingtalk.service.dingtalk_agent_service import DingtalkAgentService
from infra_dingtalk.service.dingtalk_auth_service import DingtalkAuthService
from infra_dingtalk.service.dingtalk_corp_service import DingtalkCorpService
from infra_dingtalk.service.dingtalk_k12_dept_service import DingtalkK12DeptService
from infra_dingtalk.service.dingtalk_k12_student_service import DingtalkK12StudentService
from infra_dingtalk.service.dingtalk_message_service import DingtalkMessageService
from infra_dingtalk.service.dingtalk_user_service import DingtalkUserService
from infra_dingtalk.service.plugin_service import PluginService
from infra_dingtalk.service.sync_dept_service import SyncDeptService
from infra_dingtalk.service.sync_k12_dept_service import K12SyncDeptService
from infra_dingtalk.service.sync_k12_student_service import K12SyncStudentService
from infra_dingtalk.service.sync_service import SyncService
from infra_dingtalk.service.sync_user_service import SyncUserService


class DingtalkContainer(containers.DeclarativeContainer):
    uow = providers.Dependency(instance_of=SqlAlchemyUnitOfWork)  # type: ignore

    redis_manager = providers.ThreadLocalSingleton(RedisManager)  # type: ignore

    dingtalk_agent_repository = providers.ThreadLocalSingleton(
        DingtalkAgentRepository, db_session=uow.provided.db_session
    )  # type: ignore

    dingtalk_corp_repository = providers.ThreadLocalSingleton(
        DingtalkCorpRepository, db_session=uow.provided.db_session
    )  # type: ignore

    dingtalk_dept_repository = providers.ThreadLocalSingleton(
        DingtalkDeptRepository, db_session=uow.provided.db_session
    )  # type: ignore

    dingtalk_dept_user_duty_repository = providers.ThreadLocalSingleton(
        DingtalkDeptUserDutyRepository, db_session=uow.provided.db_session
    )  # type: ignore

    dingtalk_k12_dept_repository = providers.ThreadLocalSingleton(
        DingtalkK12DeptRepository, db_session=uow.provided.db_session
    )  # type: ignore

    dingtalk_k12_dept_student_repository = providers.ThreadLocalSingleton(
        DingtalkK12DeptStudentRepository, db_session=uow.provided.db_session
    )  # type: ignore

    dingtalk_k12_family_relationship_repository = providers.ThreadLocalSingleton(
        DingtalkK12FamilyRelationshipRepository, db_session=uow.provided.db_session
    )  # type: ignore

    dingtalk_k12_parent_repository = providers.ThreadLocalSingleton(
        DingtalkK12ParentRepository, db_session=uow.provided.db_session
    )  # type: ignore

    dingtalk_k12_student_repository = providers.ThreadLocalSingleton(
        DingtalkK12StudentRepository, db_session=uow.provided.db_session
    )  # type: ignore

    dingtalk_sync_log_repository = providers.ThreadLocalSingleton(
        DingtalkSyncLogRepository, db_session=uow.provided.db_session
    )  # type: ignore

    dingtalk_user_k12_dept_duty_repository = providers.ThreadLocalSingleton(
        DingtalkUserK12DeptDutyRepository, db_session=uow.provided.db_session
    )  # type: ignore

    dingtalk_user_repository = providers.ThreadLocalSingleton(
        DingtalkUserRepository, db_session=uow.provided.db_session
    )  # type: ignore

    dingtalk_agent_service = providers.ThreadLocalSingleton(
        DingtalkAgentService, dingtalk_agent_repository=dingtalk_agent_repository
    )  # type: ignore

    plugin_service = providers.ThreadLocalSingleton(
        PluginService,
        dingtalk_agent_service=dingtalk_agent_service,
        redis_manager=redis_manager,
    )  # type: ignore

    dingtalk_corp_service = providers.ThreadLocalSingleton(
        DingtalkCorpService,
        dingtalk_corp_repository=dingtalk_corp_repository,
    )  # type: ignore

    dingtalk_auth_service = providers.ThreadLocalSingleton(
        DingtalkAuthService,
        plugin_service=plugin_service,
        dingtalk_corp_service=dingtalk_corp_service,
        dingtalk_user_repository=dingtalk_user_repository,
        dingtalk_k12_parent_repository=dingtalk_k12_parent_repository,
    )  # type: ignore

    sync_dept_service = providers.ThreadLocalSingleton(
        SyncDeptService, dingtalk_dept_repository=dingtalk_dept_repository
    )  # type: ignore

    sync_user_service = providers.ThreadLocalSingleton(
        SyncUserService,
        dingtalk_user_repository=dingtalk_user_repository,
        dingtalk_dept_user_duty_repository=dingtalk_dept_user_duty_repository,
    )  # type: ignore

    dingtalk_k12_dept_service = providers.ThreadLocalSingleton(
        DingtalkK12DeptService,
        dingtalk_k12_dept_repository=dingtalk_k12_dept_repository,
        # period_repository=period_repository,
    )  # type: ignore

    sync_k12_dept_service = providers.ThreadLocalSingleton(
        K12SyncDeptService,
        sync_user_service=sync_user_service,
        dingtalk_k12_dept_repository=dingtalk_k12_dept_repository,
        dingtalk_user_k12_dept_duty_repository=dingtalk_user_k12_dept_duty_repository,
    )  # type: ignore

    sync_k12_student_service = providers.ThreadLocalSingleton(
        K12SyncStudentService,
        dingtalk_k12_student_repository=dingtalk_k12_student_repository,
        dingtalk_k12_parent_repository=dingtalk_k12_parent_repository,
        dingtalk_k12_family_relationship_repository=dingtalk_k12_family_relationship_repository,
        dingtalk_k12_dept_student_repository=dingtalk_k12_dept_student_repository,
    )  # type: ignore

    sync_service = providers.ThreadLocalSingleton(
        SyncService,
        plugin_service=plugin_service,
        sync_user_service=sync_user_service,
        sync_dept_service=sync_dept_service,
        sync_k12_dept_service=sync_k12_dept_service,
        sync_k12_student_service=sync_k12_student_service,
    )  # type: ignore

    dingtalk_user_service = providers.ThreadLocalSingleton(
        DingtalkUserService, dingtalk_user_repository=dingtalk_user_repository
    )  # type: ignore

    dingtalk_k12_student_service = providers.ThreadLocalSingleton(
        DingtalkK12StudentService,
        dingtalk_k12_student_repository=dingtalk_k12_student_repository,
    )  # type: ignore

    dingtalk_message_service = providers.ThreadLocalSingleton(
        DingtalkMessageService,
        plugin_service=plugin_service,
        dingtalk_agent_repository=dingtalk_agent_repository,
    )  # type: ignore
