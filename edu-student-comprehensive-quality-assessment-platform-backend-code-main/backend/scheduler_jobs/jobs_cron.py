"""
定时任务方法列表
"""
import traceback

from dependency_injector.wiring import inject, Provide
from infra_basic.errors import BusinessError
from infra_basic.uow_interface import UnitOfWork
from infra_utility.datetime_helper import local_now
from loguru import logger

from backend.backend_container import BackendContainer
from context_sync.model.context_sync_log_model import (
    ContextSyncLogModel,
    EnumContextSyncDirection,
    EnumContextSyncLogCategory,
)
from context_sync.repository.context_sync_log_repository import ContextSyncLogRepository
from context_sync.service.sync_dingtalk_service import SyncDingtalkService
from infra_backbone.service.robot_service import RobotService
from infra_dingtalk.model.dingtalk_sync_log_model import (
    DingtalkSyncLogModel,
    EnumDingtalkSyncLogCategory,
    EnumDingtalkSyncLogDirection,
)
from infra_dingtalk.repository.dingtalk_sync_log_repository import DingtalkSyncLogRepository
from infra_dingtalk.service.sync_service import SyncService


@inject
def job_inner_sync(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    robot_service: RobotService = Provide[BackendContainer.backbone_container.robot_service],
    sync_service: SyncService = Provide[BackendContainer.dingtalk_container.sync_service],
    sync_log_repository: DingtalkSyncLogRepository = Provide[
        BackendContainer.dingtalk_container.dingtalk_sync_log_repository
    ],
    **kwargs,
):
    """
    内部通讯录同步
    """
    dingtalk_corp_id = None
    if kwargs.get("func_args"):
        dingtalk_corp_id = kwargs["func_args"].get("dingtalk_corp_id")
    if not dingtalk_corp_id:
        raise BusinessError("未指定同步的corp_id")
    logger.info("start inner sync")
    remark = []
    started_on = local_now()
    is_succeed = True
    err_message = None
    logger.info(started_on)
    try:
        with uow:
            handler = robot_service.get_system_robot()
            transaction = uow.log_transaction(
                handler=handler.to_basic_handler(),
                action="sync_inner_from_remote",
            )
            sync_service.sync_inner_from_remote(
                dingtalk_corp_id=dingtalk_corp_id, transaction=transaction
            )
    except Exception as err:
        remark.append(f"错误信息为：{str(err)}")
        traceback.print_exc()
        is_succeed = False
        err_message = str(err)
    try:
        with uow:
            uow.log_transaction(
                handler=robot_service.get_system_robot().to_basic_handler(),
                action="add_dingtalk_sync_log",
            )
            sync_log_repository.insert_dingtalk_sync_log(
                data=DingtalkSyncLogModel(
                    dingtalk_corp_id=dingtalk_corp_id,
                    category=EnumDingtalkSyncLogCategory.INNER.name,
                    direction=EnumDingtalkSyncLogDirection.REMOTE_TO_LOCAL.name,
                    started_on=started_on,
                    ended_on=local_now(),
                    is_succeed=is_succeed,
                    err_message=err_message,
                ),
            )
    except Exception as err:
        logger.error(err)
        traceback.print_exc()


@inject
def job_k12_sync(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    robot_service: RobotService = Provide[BackendContainer.backbone_container.robot_service],
    sync_service: SyncService = Provide[BackendContainer.dingtalk_container.sync_service],
    sync_log_repository: DingtalkSyncLogRepository = Provide[
        BackendContainer.dingtalk_container.dingtalk_sync_log_repository
    ],
    **kwargs,
):
    """
    K12通讯录同步
    """
    dingtalk_corp_id = None
    if kwargs.get("func_args"):
        dingtalk_corp_id = kwargs["func_args"].get("dingtalk_corp_id")
    if not dingtalk_corp_id:
        raise BusinessError("未指定同步的corp_id")
    logger.info("start K12 sync")
    remark = []
    started_on = local_now()
    is_succeed = True
    err_message = None
    logger.info(started_on)
    try:
        with uow:
            handler = robot_service.get_system_robot()
            transaction = uow.log_transaction(
                handler=handler.to_basic_handler(),
                action="sync_K12_from_remote",
            )
            sync_service.sync_k12_from_remote(
                dingtalk_corp_id=dingtalk_corp_id, transaction=transaction
            )
    except Exception as err:
        traceback.print_exc()
        is_succeed = False
        err_message = str(err)
    try:
        with uow:
            uow.log_transaction(
                handler=robot_service.get_system_robot().to_basic_handler(),
                action="add_dingtalk_sync_log",
            )
            sync_log_repository.insert_dingtalk_sync_log(
                data=DingtalkSyncLogModel(
                    dingtalk_corp_id=dingtalk_corp_id,
                    category=EnumDingtalkSyncLogCategory.K12.name,
                    direction=EnumDingtalkSyncLogDirection.REMOTE_TO_LOCAL.name,
                    started_on=started_on,
                    ended_on=local_now(),
                    is_succeed=is_succeed,
                    err_message=err_message,
                ),
            )
    except Exception as err:
        logger.error(err)
        traceback.print_exc()


@inject
def job_sync_dept_context(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    robot_service: RobotService = Provide[BackendContainer.backbone_container.robot_service],
    sync_context_service: SyncDingtalkService = Provide[
        BackendContainer.context_sync_container.sync_dingtalk_service
    ],
    context_sync_log_repository: ContextSyncLogRepository = Provide[
        BackendContainer.context_sync_container.context_sync_log_repository
    ],
    **kwargs,
):
    """
    上下文同步
    """
    dingtalk_corp_id = None
    if kwargs.get("func_args"):
        dingtalk_corp_id = kwargs["func_args"].get("dingtalk_corp_id")
    if not dingtalk_corp_id:
        raise BusinessError("未指定同步的corp_id")
    started_on = local_now()
    is_succeed = True
    err_message = None
    try:
        with uow:
            handler = robot_service.get_system_robot()
            transaction = uow.log_transaction(
                handler=handler.to_basic_handler(),
                action="sync_dept_context",
            )
            sync_context_service.sync_dingtalk_dept_to_master(
                dingtalk_corp_id=dingtalk_corp_id, transaction=transaction
            )
    except Exception as err:
        traceback.print_exc()
        is_succeed = False
        err_message = str(err)
    try:
        with uow:
            uow.log_transaction(
                handler=robot_service.get_system_robot().to_basic_handler(),
                action="add_context_sync_log",
            )
            direction = EnumContextSyncDirection.DINGTALK_TO_CORE.name
            context_sync_log_repository.insert_context_sync_log(
                context_sync_log=ContextSyncLogModel(
                    category=EnumContextSyncLogCategory.DEPT.name,
                    direction=direction,
                    started_on=started_on,
                    ended_on=local_now(),
                    is_succeed=is_succeed,
                    err_message=err_message,
                ),
            )
    except Exception as err:
        logger.error(err)
        traceback.print_exc()


@inject
def job_sync_inner_user_context(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    robot_service: RobotService = Provide[BackendContainer.backbone_container.robot_service],
    sync_context_service: SyncDingtalkService = Provide[
        BackendContainer.context_sync_container.sync_dingtalk_service
    ],
    context_sync_log_repository: ContextSyncLogRepository = Provide[
        BackendContainer.context_sync_container.context_sync_log_repository
    ],
    **kwargs,
):
    """
    上下文同步
    """
    dingtalk_corp_id = None
    if kwargs.get("func_args"):
        dingtalk_corp_id = kwargs["func_args"].get("dingtalk_corp_id")
    if not dingtalk_corp_id:
        raise BusinessError("未指定同步的corp_id")
    started_on = local_now()
    is_succeed = True
    err_message = None
    try:
        with uow:
            handler = robot_service.get_system_robot()
            transaction = uow.log_transaction(
                handler=handler.to_basic_handler(),
                action="sync_inner_user_context",
            )
            sync_context_service.sync_dingtalk_user_to_master(
                dingtalk_corp_id=dingtalk_corp_id, transaction=transaction
            )
    except Exception as err:
        traceback.print_exc()
        is_succeed = False
        err_message = str(err)
    try:
        with uow:
            uow.log_transaction(
                handler=robot_service.get_system_robot().to_basic_handler(),
                action="add_context_sync_log",
            )
            direction = EnumContextSyncDirection.DINGTALK_TO_CORE.name
            context_sync_log_repository.insert_context_sync_log(
                context_sync_log=ContextSyncLogModel(
                    category=EnumContextSyncLogCategory.INNER_USER.name,
                    direction=direction,
                    started_on=started_on,
                    ended_on=local_now(),
                    is_succeed=is_succeed,
                    err_message=err_message,
                ),
            )
    except Exception as err:
        logger.error(err)
        traceback.print_exc()


@inject
def job_sync_student_and_parent_context(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    robot_service: RobotService = Provide[BackendContainer.backbone_container.robot_service],
    sync_context_service: SyncDingtalkService = Provide[
        BackendContainer.context_sync_container.sync_dingtalk_service
    ],
    context_sync_log_repository: ContextSyncLogRepository = Provide[
        BackendContainer.context_sync_container.context_sync_log_repository
    ],
    **kwargs,
):
    """
    上下文同步
    """
    dingtalk_corp_id = None
    if kwargs.get("func_args"):
        dingtalk_corp_id = kwargs["func_args"].get("dingtalk_corp_id")
    if not dingtalk_corp_id:
        raise BusinessError("未指定同步的corp_id")
    started_on = local_now()
    is_succeed = True
    err_message = None
    try:
        with uow:
            handler = robot_service.get_system_robot()
            transaction = uow.log_transaction(
                handler=handler.to_basic_handler(),
                action="sync_dingtalk_parent_and_student_context",
            )
            sync_context_service.sync_dingtalk_parent_and_student_to_master(
                dingtalk_corp_id=dingtalk_corp_id, transaction=transaction
            )
    except Exception as err:
        traceback.print_exc()
        is_succeed = False
        err_message = str(err)
    try:
        with uow:
            uow.log_transaction(
                handler=robot_service.get_system_robot().to_basic_handler(),
                action="add_context_sync_log",
            )
            direction = EnumContextSyncDirection.DINGTALK_TO_CORE.name
            context_sync_log_repository.insert_context_sync_log(
                context_sync_log=ContextSyncLogModel(
                    category=EnumContextSyncLogCategory.PARENT_AND_STUDENT.name,
                    direction=direction,
                    started_on=started_on,
                    ended_on=local_now(),
                    is_succeed=is_succeed,
                    err_message=err_message,
                ),
            )
    except Exception as err:
        logger.error(err)
        traceback.print_exc()


@inject
def job_sync_context(**kwargs):
    job_sync_dept_context(**kwargs)
    job_sync_inner_user_context(**kwargs)
    job_sync_student_and_parent_context(**kwargs)


@inject
def job_sync_dingtalk(**kwargs):
    job_inner_sync(**kwargs)
    job_k12_sync(**kwargs)
