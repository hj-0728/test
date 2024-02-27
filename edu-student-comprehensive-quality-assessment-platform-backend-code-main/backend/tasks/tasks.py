import logging
import traceback
from typing import Any, Dict

from dependency_injector.wiring import inject, Provide
from infra_basic.uow_interface import UnitOfWork
from infra_pub_sub_manager.sync_pub_client import SyncPubClient
from infra_utility.serialize_helper import ORJSONPickle

from backend.backend_container import BackendContainer
from backend.data.constant import PubsubConfigConst
from backend.model.edit.command_em import CommandEditModel
from backend.service.redis_service import RedisService
from backend.service.tasks_service import TasksService
from infra_backbone.model.access_log_model import AccessLogModel
from infra_backbone.model.distributed_task_log_model import (
    DistributedTaskLogModel,
    EnumDistributedTaskLogStatus,
)
from infra_backbone.service.access_log_service import AccessLogService
from infra_backbone.service.distributed_task_log_service import DistributedTaskLogService


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
def _update_distributed_task_log(
    log: DistributedTaskLogModel,
    uow: UnitOfWork = Provide[BackendContainer.uow],
    distributed_task_log_service: DistributedTaskLogService = Provide[
        BackendContainer.backbone_container.distributed_task_log_service
    ],
    redis_service: RedisService = Provide[BackendContainer.redis_service],
):
    """
    更新分布式任务日志
    :param log:
    :param uow:
    :param distributed_task_log_service:
    :return:
    """
    try:
        transaction = uow.log_transaction(
            handler=redis_service.get_redis_robot_handler(),
            action_params={"log": log},
            action="update_distributed_task_log",
        )
        with uow:
            distributed_task_log_service.update_distributed_task_log(
                log=log, transaction=transaction
            )
        log.version += 1
    except Exception as error:
        logging.error(error)
        traceback.print_exc()


@inject
def task_handle_distributed_task(
    distributed_task_log_id: str,
    uow: UnitOfWork = Provide[BackendContainer.uow],
    tasks_service: TasksService = Provide[BackendContainer.tasks_service],
    redis_service: RedisService = Provide[BackendContainer.redis_service],
    distributed_task_log_service: DistributedTaskLogService = Provide[
        BackendContainer.backbone_container.distributed_task_log_service
    ],
    pub_client: SyncPubClient = Provide[BackendContainer.pub_client],
):
    """
    处理分布式任务
    :return:
    """
    log = distributed_task_log_service.get_distributed_task_log(log_id=distributed_task_log_id)
    try:
        log.status = EnumDistributedTaskLogStatus.IN_PROCESS.name
        max_retries = PubsubConfigConst.MAX_RETRIES
        for i in range(max_retries):
            log.try_count += 1
            try:
                transaction = uow.log_transaction(
                    handler=redis_service.get_redis_robot_handler(),
                    action_params={"log": log},
                    action="task_handle_distributed_task",
                )
                with uow:
                    new_log_ids = tasks_service.execute_task(
                        distributed_task_log=log, transaction=transaction
                    )

                # 任务完成，需要通知其他异步事务接着处理
                if new_log_ids:
                    for new_log_id in new_log_ids:
                        command = CommandEditModel(
                            category="task_handle_distributed_task", args=new_log_id
                        )
                        pub_client.send_message(message=ORJSONPickle.encode_model(command))
                break  # 如果任务成功，跳出循环
            except Exception as error:
                if i == max_retries - 1:  # 如果已经达到最大尝试次数，记录失败并结束
                    raise
                else:  # 如果尚未达到最大尝试次数，继续尝试
                    log.err_msg = str(error)
                    _update_distributed_task_log(log=log)
    except Exception as error:
        logging.error(error)
        traceback.print_exc()
        log.err_msg = str(error)
        log.status = EnumDistributedTaskLogStatus.FAILED.name
        _update_distributed_task_log(log=log)
    else:
        log.err_msg = None
        log.status = EnumDistributedTaskLogStatus.SUCCEED.name
        _update_distributed_task_log(log=log)
