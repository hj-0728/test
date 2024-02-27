import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.basic_repository import PageFilterParams
from infra_basic.errors import BusinessError
from infra_basic.message_carrier import MessageCarrier
from infra_basic.uow_interface import UnitOfWork

from backend.backend_containers import BackendContainer
from backend.blueprint import get_current_handler, get_current_role_code, get_current_user_id
from backend.data.constant import FlaskConfigConst
from backend.service.app_role_service import AppRoleService
from backend.service.redis_service import RedisService
from infra_backbone.model.role_model import RoleModel
from infra_backbone.service.role_service import RoleService

blueprint_role = Blueprint(
    name="role",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/role"


@blueprint_role.route(f"{WEB_PREFIX}/update-user-current-role", methods=["POST"])
@inject
def route_update_user_current_role(
    redis_service: RedisService = Provide[BackendContainer.redis_service],
) -> jsonify:
    """
    更新用户当前角色
    :return:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        role_id = data.get("roleId", None)
        if not role_id:
            raise BusinessError("未找到")
        redis_service.update_redis_user_profile_current_role(
            role_id=role_id,
            user_id=get_current_user_id(),
        )
        carrier.push_succeed_data(data=True)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict())


@blueprint_role.route(f"{WEB_PREFIX}/page-list", methods=["POST"])
@inject
def route_get_role_list(
    role_service: RoleService = Provide[BackendContainer.backbone_container.role_service],
):
    """
    获取角色列表
    """
    carrier = MessageCarrier()
    try:
        query_params = request.get_json(silent=True)
        role_list = role_service.get_role_list_page_info(
            query_params=PageFilterParams(**query_params),
            role_code=get_current_role_code(),
        )
        carrier.push_succeed_data(data=role_list)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_role.route(f"{WEB_PREFIX}/change-is-activated", methods=["POST"])
@inject
def route_change_is_activated(
    role_service: RoleService = Provide[BackendContainer.backbone_container.role_service],
    uow: UnitOfWork = Provide[BackendContainer.uow],
):
    """
    改变激活状态
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        role = RoleModel(**data)
        transaction = uow.log_transaction(
            handler=get_current_handler(),
            action="update_role_is_activated",
            action_params=data,
        )
        role_service.change_is_activated(role=role, transaction=transaction)
        carrier.push_succeed_data()
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict())


@blueprint_role.route(f"{WEB_PREFIX}/info/<string:role_id>", methods=["GET"])
@inject
def route_get_role_info(
    role_id: str,
    role_service: RoleService = Provide[BackendContainer.backbone_container.role_service],
):
    """
    获取角色的基本信息
    """
    carrier = MessageCarrier()
    try:
        role_info = role_service.get_role_info(
            role_id=role_id,
        )
        carrier.push_succeed_data(data=role_info)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_role.route(f"{WEB_PREFIX}/save", methods=["POST"])
@inject
def route_add_or_update_role(
    role_service: RoleService = Provide[BackendContainer.backbone_container.role_service],
    uow: UnitOfWork = Provide[BackendContainer.uow],
):
    """
    添加或修改角色
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        role_em = RoleModel(**data)
        transaction = uow.log_transaction(
            handler=get_current_handler(),
            action="save_or_update_role",
            action_params=data,
        )
        role_service.save_role(role=role_em, transaction=transaction)
        carrier.push_succeed_data()
    except BusinessError as err:
        carrier.push_exception(err=err)
        traceback.print_exc()
    return jsonify(carrier.dict())


@blueprint_role.route(f"{WEB_PREFIX}/get-role-filter-list", methods=["GET"])
@inject
def route_get_role_filter_list(
    role_service: RoleService = Provide[BackendContainer.backbone_container.role_service],
):
    carrier = MessageCarrier()
    try:
        role_list = role_service.get_role_filter_list(role_code=get_current_role_code())
        carrier.push_succeed_data(data=role_list)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict())


@blueprint_role.route(f"{WEB_PREFIX}/get-teacher-role-list", methods=["GET"])
@inject
def route_get_teacher_role_list(
    app_role_service: AppRoleService = Provide[BackendContainer.app_role_service],
):
    """
    获取教师角色列表 (即除了学生的角色)
    :param app_role_service:
    :return:
    """
    carrier = MessageCarrier()
    try:
        role_list = app_role_service.get_teacher_role_list(role_code=get_current_role_code())
        carrier.push_succeed_data(data=role_list)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict())
