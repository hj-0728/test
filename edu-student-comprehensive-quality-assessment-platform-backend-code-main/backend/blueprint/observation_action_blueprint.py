import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.errors import BusinessError
from infra_basic.message_carrier import MessageCarrier
from infra_basic.uow_interface import UnitOfWork
from infra_pub_sub_manager.sync_pub_client import SyncPubClient
from infra_utility.serialize_helper import ORJSONPickle

from backend.backend_container import BackendContainer
from backend.blueprint import get_current_handler, get_current_people_id
from backend.data.constant import FlaskConfigConst
from backend.model.edit.command_em import CommandEditModel
from biz_comprehensive.data.enum import EnumComprehensiveResource
from biz_comprehensive.model.edit.observation_action_em import SaveEvaluationObsActionEditModel
from biz_comprehensive.model.observation_action_model import EnumPerformerResCategory
from biz_comprehensive.service.observation_action_service import ObservationActionService
from infra_backbone.model.distributed_task_log_model import DistributedTaskLogModel
from infra_backbone.service.distributed_task_log_service import DistributedTaskLogService

blueprint_observation_action = Blueprint(
    name="observation_action", import_name=__name__, url_prefix=f"{FlaskConfigConst.API_PREFIX}"
)

MOBILE_PREFIX = "/mobile/observation-action"


@blueprint_observation_action.route(f"{MOBILE_PREFIX}/delete/<string:action_id>", methods=["POST"])
@inject
def route_delete_observation_action(
    action_id: str,
    uow: UnitOfWork = Provide[BackendContainer.uow],
    observation_action_service: ObservationActionService = Provide[
        BackendContainer.comprehensive_container.observation_action_service
    ],
    distributed_task_log_service: DistributedTaskLogService = Provide[
        BackendContainer.backbone_container.distributed_task_log_service
    ],
    pub_client: SyncPubClient = Provide[BackendContainer.pub_client],
):
    """
    删除观察点日志
    :param action_id:
    :param observation_action_service:
    :param uow:
    :param pub_client:
    :param distributed_task_log_service:
    :return:
    """
    carrier = MessageCarrier()
    try:
        transaction = uow.log_transaction(
            handler=get_current_handler(),
            action_params={"observation_action_id": action_id},
            action="delete_observation_action",
        )
        log_ids = []
        with uow:
            produce_list = observation_action_service.delete_observation_action(
                action_id=action_id, transaction=transaction
            )
            # 推pubsub，做后续处理
            for produce in produce_list:
                # 原则上task_func不应该这样写死，应该根据produce_res_category从某处配置中匹配，
                # 但是目前只这一种情况，且短期未预想到可能的变化，所以先这样写，若后续业务有不支持的再做相应的调整
                log = {
                    "source_res_category": produce.produce_res_category,
                    "source_res_id": produce.produce_res_id,
                    "task_func": "task_revoke_points",
                }
                log_id = distributed_task_log_service.add_distributed_task_log(
                    log=DistributedTaskLogModel(**log), transaction=transaction
                )
                log_ids.append(log_id)
            log = {
                "source_res_category": EnumComprehensiveResource.OBSERVATION_ACTION.name,
                "source_res_id": action_id,
                "task_func": "task_delete_snapshot",
            }
            log_id = distributed_task_log_service.add_distributed_task_log(
                log=DistributedTaskLogModel(**log), transaction=transaction
            )
            log_ids.append(log_id)
        for log_id in log_ids:
            command = CommandEditModel(category="task_handle_distributed_task", args=log_id)
            pub_client.send_message(message=ORJSONPickle.encode_model(command))
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_observation_action.route(
    f"{MOBILE_PREFIX}/save-evaluation-action", methods=["POST"]
)
@inject
def route_save_evaluation_observation_action(
    observation_action_service: ObservationActionService = Provide[
        BackendContainer.comprehensive_container.observation_action_service
    ],
    uow: UnitOfWork = Provide[BackendContainer.uow],
    distributed_task_log_service: DistributedTaskLogService = Provide[
        BackendContainer.backbone_container.distributed_task_log_service
    ],
    pub_client: SyncPubClient = Provide[BackendContainer.pub_client],
):
    """
    保存评价观察动作
    :param observation_action_service:
    :param uow:
    :param distributed_task_log_service:
    :param pub_client:
    :return:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        transaction = uow.log_transaction(
            handler=get_current_handler(),
            action_params=data,
            action="save_evaluation_observation_action",
        )
        log_ids = []
        with uow:
            action_info = SaveEvaluationObsActionEditModel(**data)
            action_info.performer_res_id = get_current_people_id()
            action_info.performer_res_category = EnumPerformerResCategory.PEOPLE.name
            produce_list = observation_action_service.save_evaluation_observation_action(
                action_info=action_info, transaction=transaction
            )

            for produce in produce_list:
                log = {
                    "source_res_category": produce.res_category,
                    "source_res_id": produce.res_id,
                    "task_func": "task_save_calc",
                }
                log_id = distributed_task_log_service.add_distributed_task_log(
                    log=DistributedTaskLogModel(**log), transaction=transaction
                )
                log_ids.append(log_id)
        for log_id in log_ids:
            command = CommandEditModel(category="task_handle_distributed_task", args=log_id)
            pub_client.send_message(message=ORJSONPickle.encode_model(command))

    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))
