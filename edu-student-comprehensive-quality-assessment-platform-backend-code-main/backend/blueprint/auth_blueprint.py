import copy
import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.errors import BusinessError
from infra_basic.message_carrier import MessageCarrier
from infra_basic.uow_interface import UnitOfWork
from loguru import logger

from backend.backend_container import BackendContainer
from backend.blueprint import get_current_user_id, get_robot_handler
from backend.data.constant import FlaskConfigConst
from backend.model.edit.user_login_data_em import UserLoginDataEditModel
from backend.service.app_menu_service import AppMenuService
from backend.service.app_role_service import AppRoleService
from backend.service.auth_service import AuthService
from infra_backbone.model.menu_model import EnumMenuCategory

blueprint_auth = Blueprint(
    name="auth", import_name=__name__, url_prefix=f"{FlaskConfigConst.API_PREFIX}"
)

WEB_PREFIX = "/web/auth"
MOBILE_PREFIX = "/mobile/auth"



@blueprint_auth.route(f"{WEB_PREFIX}/login", methods=["POST"])
@inject
def route_login(
    auth_service: AuthService = Provide[BackendContainer.auth_service],
    uow: UnitOfWork = Provide[BackendContainer.uow],
):
    """
    登录
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
            result = auth_service.login(
                user_params=UserLoginDataEditModel(**user_info), transaction=transaction
            )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_auth.route(f"{WEB_PREFIX}/get-user-sidebar-menu", methods=["GET"])
@inject
def route_get_user_sidebar_menu(
    app_menu_service: AppMenuService = Provide[BackendContainer.app_menu_service],
    role_service: AppRoleService = Provide[BackendContainer.app_role_service],
):
    """
    获取用户侧边栏菜单
    """
    carrier = MessageCarrier()
    try:
        data = app_menu_service.get_user_sidebar_menu(
            role_id=role_service.get_current_role_id(),
            menu_category=EnumMenuCategory.WEB.name,
        )
        carrier.push_succeed_data(data=data)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_auth.route(f"{WEB_PREFIX}/get-current-user-info", methods=["GET"])
@inject
def route_get_current_user_info(
    auth_service: AuthService = Provide[BackendContainer.auth_service],
):
    """
    获取当前用户信息
    """
    carrier = MessageCarrier()
    try:
        data = auth_service.get_current_user_info(user_id=get_current_user_id())
        carrier.push_succeed_data(data=data)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_auth.route(
    f"{MOBILE_PREFIX}/dingtalk-login/<string:code>/<string:desired_identity>", methods=["POST"]
)
@inject
def route_dingtalk_login(
    code: str,
    desired_identity: str,
    auth_service: AuthService = Provide[BackendContainer.auth_service],
):
    """
    钉钉登录
    """
    carrier = MessageCarrier()
    try:
        logger.info(f"身份验证code值【{code}】，期望的身份【{desired_identity}】")
        data = auth_service.get_dingtalk_oauth_jwt_token(
            code=code, desired_identity=desired_identity
        )
        carrier.push_succeed_data(data=data)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_auth.route(f"{MOBILE_PREFIX}/dev-login", methods=["POST"])
@inject
def route_dev_login(auth_service: AuthService = Provide[BackendContainer.auth_service]):
    """
    dev用户登录
    """
    carrier = MessageCarrier()
    try:
        data = auth_service.get_dev_user_login_token()
        carrier.push_succeed_data(data=data)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_auth.route(f"{WEB_PREFIX}/get-login-validate-image", methods=["GET"])
@inject
def route_get_login_validate_image(
    auth_service: AuthService = Provide[BackendContainer.auth_service],
):
    """
    获取图像验证码
    :param auth_service:
    :return:
    """
    carrier = MessageCarrier()
    try:
        image_src = auth_service.create_verify_image_for_login()
        carrier.push_succeed_data(data=image_src)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))
