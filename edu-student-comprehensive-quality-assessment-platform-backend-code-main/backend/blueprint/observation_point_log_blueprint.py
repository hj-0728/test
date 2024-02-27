import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify
from infra_basic.errors import BusinessError
from infra_basic.message_carrier import MessageCarrier
from infra_basic.uow_interface import UnitOfWork

from backend.backend_container import BackendContainer
from backend.blueprint import get_current_handler
from backend.data.constant import FlaskConfigConst
from biz_comprehensive.service.observation_point_log_service import ObservationPointLogService

blueprint_observation_point_log = Blueprint(
    name="observation_point_log", import_name=__name__, url_prefix=f"{FlaskConfigConst.API_PREFIX}"
)

MOBILE_PREFIX = "/mobile/observation-point-log"


@blueprint_observation_point_log.route(f"{MOBILE_PREFIX}/delete/<string:log_id>", methods=["POST"])
@inject
def route_delete_observation_point_log(
    log_id: str,
    observation_point_log_service: ObservationPointLogService = Provide[
        BackendContainer.comprehensive_container.observation_point_log_service
    ],
    uow: UnitOfWork = Provide[BackendContainer.uow],
):
    """
    删除观察点日志
    :param log_id:
    :param observation_point_log_service:
    :param uow:
    :return:
    """
    carrier = MessageCarrier()
    try:
        transaction = uow.log_transaction(
            handler=get_current_handler(),
            action_params={"observation_point_log_id": log_id},
            action="delete_observation_point_log",
        )
        with uow:
            observation_point_log_service.delete_observation_point_log(
                log_id=log_id, transaction=transaction
            )
        # todo 此处还要推pubsub去反冲积分
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))
