import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.errors import BusinessError
from infra_basic.message_carrier import MessageCarrier
from infra_basic.uow_interface import UnitOfWork

from backend.backend_container import BackendContainer
from backend.blueprint import get_current_handler, get_current_people_id
from backend.data.constant import FlaskConfigConst
from biz_comprehensive.model.edit.save_observation_point_em import SaveObservationPointEditModel
from biz_comprehensive.model.param.scence_observation_point_query_params import (
    SceneObservationPointQueryParams,
)
from biz_comprehensive.service.observation_point_service import ObservationPointService

blueprint_observation_point = Blueprint(
    name="observation_point", import_name=__name__, url_prefix=f"{FlaskConfigConst.API_PREFIX}"
)

WEB_PREFIX = "/web/observation-point"
MOBILE_PREFIX = "/mobile/observation-point"


@blueprint_observation_point.route(f"{WEB_PREFIX}/list", methods=["GET"])
@inject
def route_get_observation_point_list(
    observation_point_service: ObservationPointService = Provide[
        BackendContainer.comprehensive_container.observation_point_service
    ],
):
    """
    获取观测点列表
    :param observation_point_service:
    :return:
    """
    carrier = MessageCarrier()
    try:
        observation_point_list = observation_point_service.get_observation_point_list()
        carrier.push_succeed_data(data=observation_point_list)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_observation_point.route(f"{WEB_PREFIX}/save", methods=["POST"])
@inject
def route_save_observation_point(
    observation_point_service: ObservationPointService = Provide[
        BackendContainer.comprehensive_container.observation_point_service
    ],
    uow: UnitOfWork = Provide[BackendContainer.uow],
):
    """
    保存观测点
    :param observation_point_service:
    :param uow:
    :return:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        observation_point = SaveObservationPointEditModel(**data)
        transaction = uow.log_transaction(
            handler=get_current_handler(),
            action="save_observation_point",
            action_params=data,
        )
        with uow:
            observation_point_service.save_observation_point(
                observation_point=observation_point, transaction=transaction
            )
        carrier.push_succeed_data()
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_observation_point.route(f"{WEB_PREFIX}/delete", methods=["POST"])
@inject
def route_delete_observation_point(
    observation_point_service: ObservationPointService = Provide[
        BackendContainer.comprehensive_container.observation_point_service
    ],
    uow: UnitOfWork = Provide[BackendContainer.uow],
):
    """
    删除观测点
    :param observation_point_service:
    :param uow:
    :return:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        observation_point_id = data.get("id")
        transaction = uow.log_transaction(
            handler=get_current_handler(),
            action="delete_observation_point",
            action_params=data,
        )
        with uow:
            observation_point_service.delete_observation_point(
                observation_point_id=observation_point_id, transaction=transaction
            )
        carrier.push_succeed_data()
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_observation_point.route(
    f"{WEB_PREFIX}/get-system-icon/<string:category>", methods=["GET"]
)
@inject
def route_get_observation_point_system_icon(
    category: str,
    observation_point_service: ObservationPointService = Provide[
        BackendContainer.comprehensive_container.observation_point_service
    ],
):
    """
    获取系统图标
    :param category:
    :param observation_point_service:
    :return:
    """
    carrier = MessageCarrier()
    try:
        icon_list = observation_point_service.get_observation_point_system_icon(category=category)
        carrier.push_succeed_data(data=icon_list)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_observation_point.route(
    f"{WEB_PREFIX}/get-observation-point/<string:observation_point_id>", methods=["GET"]
)
@inject
def route_get_observation_point_info(
    observation_point_id: str,
    observation_point_service: ObservationPointService = Provide[
        BackendContainer.comprehensive_container.observation_point_service
    ],
):
    """
    获取观测点信息
    :param observation_point_id:
    :param observation_point_service:
    :return:
    """
    carrier = MessageCarrier()
    try:
        observation_point = observation_point_service.get_observation_point_info(
            observation_point_id=observation_point_id
        )
        carrier.push_succeed_data(data=observation_point)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_observation_point.route(f"{MOBILE_PREFIX}/by-scene-id", methods=["POST"])
@inject
def route_get_observation_point_list_by_scene_id(
    observation_point_service: ObservationPointService = Provide[
        BackendContainer.comprehensive_container.observation_point_service
    ],
):
    """
    获取场景下的观测点列表
    :param observation_point_service:
    :return:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        result = observation_point_service.get_observation_point_list_by_scene_id(
            params=SceneObservationPointQueryParams(**data),
            people_id=get_current_people_id(),
        )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))
