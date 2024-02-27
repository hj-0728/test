import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.errors import BusinessError
from infra_basic.message_carrier import MessageCarrier
from infra_basic.uow_interface import UnitOfWork

from backend.backend_container import BackendContainer
from backend.blueprint import get_current_handler, get_current_people_id
from backend.data.constant import FlaskConfigConst
from biz_comprehensive.model.edit.scene_em import SceneEditModel
from biz_comprehensive.model.param.scence_statistics_query_params import SceneStatisticsQueryParams
from biz_comprehensive.service.scene_service import SceneService

blueprint_scene = Blueprint(
    name="scene", import_name=__name__, url_prefix=f"{FlaskConfigConst.API_PREFIX}"
)

WEB_PREFIX = "/web/scene"
MOBILE_PREFIX = "/mobile/scene"


@blueprint_scene.route(f"{WEB_PREFIX}/save", methods=["POST"])
@inject
def route_save_scene(
    scene_service: SceneService = Provide[BackendContainer.comprehensive_container.scene_service],
    uow: UnitOfWork = Provide[BackendContainer.uow],
):
    """
    新增或修改场景
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        transaction = uow.log_transaction(
            handler=get_current_handler(),
            action="save_scene",
            action_params=data,
        )
        with uow:
            scene_id = scene_service.add_or_update_scene(
                scene_em=SceneEditModel(**data),
                transaction=transaction,
            )
        carrier.push_succeed_data(data=scene_id)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_scene.route(f"{WEB_PREFIX}/list", methods=["GET"])
@inject
def route_get_scene_list(
    scene_service: SceneService = Provide[BackendContainer.comprehensive_container.scene_service],
):
    """
    获取场景列表
    """
    carrier = MessageCarrier()
    try:
        scene_list = scene_service.get_scene_list()
        carrier.push_succeed_data(data=scene_list)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_scene.route(f"{WEB_PREFIX}/delete", methods=["POST"])
@inject
def route_delete_scene(
    scene_service: SceneService = Provide[BackendContainer.comprehensive_container.scene_service],
    uow: UnitOfWork = Provide[BackendContainer.uow],
):
    """
    删除场景
    """

    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        transaction = uow.log_transaction(
            handler=get_current_handler(),
            action="delete_scene",
            action_params=data,
        )
        with uow:
            scene_id = scene_service.delete_scene_by_scene_id(
                scene_id=data.get("sceneId"),
                transaction=transaction,
            )
        carrier.push_succeed_data(data=scene_id)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_scene.route(f"{MOBILE_PREFIX}/with-observation-point-count/<string:terminal>", methods=["GET"])
@inject
def route_get_scene_with_observation_point_count(
    terminal: str,
    scene_service: SceneService = Provide[BackendContainer.comprehensive_container.scene_service],
):
    """
    获取场景列表带有观测点数量
    :param terminal:
    :param scene_service:
    :return:
    """
    carrier = MessageCarrier()
    try:
        result = scene_service.get_scene_with_observation_point_count(
            people_id=get_current_people_id(),
            terminal=terminal
        )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_scene.route(f"{WEB_PREFIX}/terminal-category-list", methods=["GET"])
@inject
def route_get_scene_terminal_category_list(
    scene_service: SceneService = Provide[BackendContainer.comprehensive_container.scene_service],
):
    """
    获取场景终端类型列表
    """
    carrier = MessageCarrier()
    try:
        scene_list = scene_service.get_scene_terminal_category_list()
        carrier.push_succeed_data(data=scene_list)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_scene.route(f"{WEB_PREFIX}/info/<string:scene_id>", methods=["GET"])
@inject
def route_get_scene_info_by_id(
    scene_id: str,
    scene_service: SceneService = Provide[BackendContainer.comprehensive_container.scene_service],
):
    """
    根据场景id获取场景信息
    """
    carrier = MessageCarrier()
    try:
        scene_info = scene_service.get_scene_info_by_scene_id(scene_id=scene_id)
        carrier.push_succeed_data(data=scene_info)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))
