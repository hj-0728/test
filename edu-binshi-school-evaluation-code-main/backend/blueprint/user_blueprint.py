import copy
import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from infra_basic.errors import BusinessError
from infra_basic.message_carrier import MessageCarrier
from infra_basic.uow_interface import UnitOfWork

from backend.backend_containers import BackendContainer
from backend.blueprint import get_current_handler, get_current_user_id, get_robot_handler
from backend.data.constant import FlaskConfigConst
from backend.model.edit.user_login_data_em import UserLoginDataEditModel
from backend.model.edit.user_reset_password_em import UserResetPasswordEditModel
from backend.service.app_role_service import AppRoleService
from backend.service.app_user_service import AppUserService
from backend.service.redis_service import RedisService
from infra_backbone.data.constant import RedisConst, SymbolConst
from infra_backbone.model.edit.user_password_em import (
    ImproveUserPasswordEditModel,
    UserPasswordEditModel,
)
from infra_backbone.model.params.user_params import UserQueryParams
from infra_backbone.model.user_model import UserModel
from infra_backbone.service.user_service import UserService

blueprint_user = Blueprint(
    name="user",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/user"


@blueprint_user.route(f"{WEB_PREFIX}/list", methods=["POST"])
@inject
def route_get_user_list(
    user_service: UserService = Provide[BackendContainer.backbone_container.user_service],
):
    """
    获取用户列表
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        result = user_service.get_user_list(
            params=UserQueryParams(**data),
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_user.route(f"{WEB_PREFIX}/add", methods=["POST"])
@inject
def route_add_user(
    user_service: UserService = Provide[BackendContainer.backbone_container.user_service],
    uow: UnitOfWork = Provide[BackendContainer.uow],
):
    """
    添加用户
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        transaction = uow.log_transaction(
            handler=get_current_handler(),
            action="add_user",
            action_params={"user": data},
        )
        with uow:
            user_service.add_user(
                user=UserModel(**data),
                transaction=transaction,
            )
        carrier.push_succeed_data()
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_user.route(f"{WEB_PREFIX}/edit", methods=["POST"])
@inject
def route_edit_user(
    user_service: AppUserService = Provide[BackendContainer.app_user_service],
    uow: UnitOfWork = Provide[BackendContainer.uow],
):
    """
    编辑用户
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        transaction = uow.log_transaction(
            handler=get_current_handler(),
            action="edit_user",
            action_params=data,
        )
        with uow:
            user_service.edit_user(
                data=UserModel(**data),
                transaction=transaction,
            )
        carrier.push_succeed_data(data={"logout": data["id"] == get_current_user_id()})
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_user.route(f"{WEB_PREFIX}/chang-user-activated", methods=["POST"])
@inject
def route_chang_user_activated(
    app_user_service: AppUserService = Provide[BackendContainer.app_user_service],
    uow: UnitOfWork = Provide[BackendContainer.uow],
) -> jsonify:
    """
    改变用户激活状态
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        transaction = uow.log_transaction(
            handler=get_current_handler(),
            action="chang_user_activated",
            action_params=data,
        )
        with uow:
            app_user_service.update_user_activated(
                user=UserModel(**data),
                transaction=transaction,
            )
            carrier.push_succeed_data(data=True)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_user.route(f"{WEB_PREFIX}/reset-password", methods=["POST"])
@inject
def route_reset_password(
    app_user_service: AppUserService = Provide[BackendContainer.app_user_service],
    uow: UnitOfWork = Provide[BackendContainer.uow],
):
    """
    重置用户密码
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        transaction = uow.log_transaction(
            handler=get_current_handler(), action="reset_password", action_params=data
        )
        with uow:
            new_password = app_user_service.reset_password(
                data=UserResetPasswordEditModel(**data),
                transaction=transaction,
            )
            carrier.push_succeed_data(data=new_password)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_user.route(f"{WEB_PREFIX}/login", methods=["POST"])
@inject
def route_user_login(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    app_user_service: AppUserService = Provide[BackendContainer.app_user_service],
):
    """
    用户登录
    :return:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        user_info = copy.deepcopy(data)
        if "password" in data:
            data.pop("password")
        transaction = uow.log_transaction(
            handler=get_robot_handler(),
            action="user_login",
            action_params=data,
        )
        with uow:
            result = app_user_service.user_login(
                user_params=UserLoginDataEditModel(**user_info), transaction=transaction
            )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_user.route(f"{WEB_PREFIX}/get-user-info", methods=["GET"])
@inject
def route_get_user_info(
    user_service: UserService = Provide[BackendContainer.backbone_container.user_service],
    app_role_service: AppRoleService = Provide[BackendContainer.app_role_service],
):
    """
    获取用户信息
    :return:
    """
    carrier = MessageCarrier()
    try:
        result = user_service.get_user_info(
            user_id=get_current_user_id(), role_id=app_role_service.get_current_role_id()
        )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_user.route(f"{WEB_PREFIX}/logout", methods=["POST"])
@jwt_required()
@inject
def route_user_logout(
    app_user_service: AppUserService = Provide[BackendContainer.app_user_service],
    redis_service: RedisService = Provide[BackendContainer.redis_service],
) -> jsonify:
    """
    用户登出
    :return:
    """
    carrier = MessageCarrier()
    try:
        app_user_service.set_black_list()
        redis_key = RedisConst.SESSION + SymbolConst.COLON + get_jwt_identity()
        redis_service.delete(key=redis_key)
        carrier.push_succeed_data(data=True)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_user.route(f"{WEB_PREFIX}/get-login-validate-image", methods=["GET"])
@inject
def route_get_login_validate_image(
    app_user_service: AppUserService = Provide[BackendContainer.app_user_service],
):
    """
    获取图像验证码
    :param app_user_service:
    :return:
    """
    carrier = MessageCarrier()
    try:
        image_src = app_user_service.create_verify_image_for_login()
        carrier.push_succeed_data(data=image_src)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_user.route(f"{WEB_PREFIX}/change-user-password", methods=["POST"])
@inject
def route_change_user_password(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    app_user_service: AppUserService = Provide[BackendContainer.app_user_service],
) -> jsonify:
    """
    修改用户密码
    :return:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        transaction = uow.log_transaction(
            handler=get_current_handler(),
            action="change_user_password",
        )
        with uow:
            app_user_service.change_user_password(
                user_password=UserPasswordEditModel(**data),
                transaction=transaction,
                user_id=get_current_user_id(),
            )
            app_user_service.set_black_list()
        carrier.push_succeed_data()
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict())


@blueprint_user.route(f"{WEB_PREFIX}/improve-user-password", methods=["POST"])
@inject
def route_improve_user_password(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    user_service: UserService = Provide[BackendContainer.backbone_container.user_service],
) -> jsonify:
    """
    完善用户密码
    :return:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        transaction = uow.log_transaction(
            handler=get_current_handler(),
            action="improve_user_password",
        )
        with uow:
            result = user_service.improve_user_password(
                user_password=ImproveUserPasswordEditModel(**data),
                transaction=transaction,
                user_id=get_current_user_id(),
            )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict())


@blueprint_user.route(f"{WEB_PREFIX}/teacher-list", methods=["POST"])
@inject
def route_get_teacher_list(
    app_user_service: AppUserService = Provide[BackendContainer.app_user_service],
):
    """
    获取用户列表
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        result = app_user_service.get_teacher_list(
            params=UserQueryParams(**data),
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))
