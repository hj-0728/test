import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.errors import BusinessError
from infra_basic.message_carrier import MessageCarrier
from infra_basic.uow_interface import UnitOfWork
from infra_utility.enum_helper import enum_to_dict_list

from backend.backend_containers import BackendContainer
from backend.blueprint import get_current_handler
from backend.data.constant import FlaskConfigConst
from infra_backbone.model.params.route_query_params import RouteQueryParams
from infra_backbone.model.route_model import EnumRouteAccessStrategy, RouteModel
from infra_backbone.service.route_service import RouteService

blueprint_route = Blueprint(
    name="route",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/route"


@blueprint_route.route(f"{WEB_PREFIX}/list", methods=["POST"])
@inject
def route_get_path_list(
    route_service: RouteService = Provide[BackendContainer.backbone_container.route_service],
):
    """
    获取路径列表
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        result = route_service.get_path_list(query_params=RouteQueryParams(**data))
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_route.route(f"{WEB_PREFIX}/edit", methods=["POST"])
@inject
def route_edit_path(
    route_service: RouteService = Provide[BackendContainer.backbone_container.route_service],
    uow: UnitOfWork = Provide[BackendContainer.uow],
):
    """
    编辑路径
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        trans = uow.log_transaction(
            handler=get_current_handler(),
            action="edit_path",
            action_params=data,
        )
        with uow:
            route_service.edit_path(
                data=RouteModel(**data),
                transaction=trans,
            )
            carrier.push_succeed_data(data=True)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_route.route(f"{WEB_PREFIX}/access-strategy", methods=["GET"])
def route_get_route_access_strategy():
    """
    获取路径身份验证
    """
    carrier = MessageCarrier()
    try:
        result = enum_to_dict_list(EnumRouteAccessStrategy)
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_route.route(f"{WEB_PREFIX}/assign-tree/<string:route_id>", methods=["GET"])
@inject
def route_get_route_ability_permission_assign_tree(
    route_id,
    route_service: RouteService = Provide[BackendContainer.backbone_container.route_service],
):
    """
    获取路径列表
    """
    carrier = MessageCarrier()
    try:
        result = route_service.get_route_ability_permission_assign_tree(route_id=route_id)
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))
