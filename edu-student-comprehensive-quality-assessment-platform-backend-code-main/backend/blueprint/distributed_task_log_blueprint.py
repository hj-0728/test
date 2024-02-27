import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.message_carrier import MessageCarrier
from infra_basic.uow_interface import UnitOfWork
from infra_pub_sub_manager.sync_pub_client import SyncPubClient
from infra_utility.serialize_helper import ORJSONPickle

from backend.backend_container import BackendContainer
from backend.blueprint import get_robot_handler
from backend.data.constant import FlaskConfigConst
from backend.model.edit.command_em import CommandEditModel
from infra_backbone.model.distributed_task_log_model import DistributedTaskLogModel
from infra_backbone.service.distributed_task_log_service import DistributedTaskLogService

blueprint_distributed_task_log = Blueprint(
    name="distributed_task_log", import_name=__name__, url_prefix=f"{FlaskConfigConst.API_PREFIX}"
)

MOBILE_PREFIX = "/mobile/distributed-task-log"


@blueprint_distributed_task_log.route(f"{MOBILE_PREFIX}/add", methods=["POST"])
@inject
def route_add_distributed_task_log(
    distributed_task_log: DistributedTaskLogService = Provide[
        BackendContainer.backbone_container.distributed_task_log_service
    ],
    uow: UnitOfWork = Provide[BackendContainer.uow],
    pub_client: SyncPubClient = Provide[BackendContainer.pub_client],
):
    """
    添加分布式任务日志
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        transaction = uow.log_transaction(
            handler=get_robot_handler(), action_params=data, action="add_distributed_task_log"
        )
        with uow:
            log_id = distributed_task_log.add_distributed_task_log(
                log=DistributedTaskLogModel(**data), transaction=transaction
            )
        command = CommandEditModel(category="task_handle_distributed_task", args=log_id)
        pub_client.send_message(message=ORJSONPickle.encode_model(command))
        carrier.push_succeed_data()
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_distributed_task_log.route(f"{MOBILE_PREFIX}/push/<string:log_id>", methods=["POST"])
@inject
def route_push_distributed_task_log(
    log_id: str,
    pub_client: SyncPubClient = Provide[BackendContainer.pub_client],
):
    """
    推送分布式任务日志
    """
    carrier = MessageCarrier()
    try:
        command = CommandEditModel(category="task_handle_distributed_task", args=log_id)
        pub_client.send_message(message=ORJSONPickle.encode_model(command))
        carrier.push_succeed_data()
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))
