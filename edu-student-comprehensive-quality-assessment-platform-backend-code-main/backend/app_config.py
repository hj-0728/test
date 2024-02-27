import copy
import json
import traceback
from typing import Any, List, Optional

from dependency_injector.wiring import inject, Provide
from flask import current_app, Flask, jsonify, request, Response
from flask_jwt_extended import verify_jwt_in_request
from infra_basic.errors.entity import EntityNotFoundError
from infra_basic.errors.permission import NeedLoginError, NotPermissionError
from infra_basic.message_carrier import MessageCarrier
from infra_basic.sqlalchemy_uow import SqlAlchemyUnitOfWork
from infra_basic.uow_interface import UnitOfWork
from infra_pub_sub_manager.sync_pub_client import SyncPubClient
from infra_utility.datetime_helper import local_now
from infra_utility.lang_helper import ErrorInfo
from infra_utility.serialize_helper import ORJSONPickle
from jwt import ExpiredSignatureError
from loguru import logger
from sqlalchemy.orm import Session

from backend.backend_container import BackendContainer
from backend.blueprint import get_current_handler, get_robot_handler
from backend.model.edit.command_em import CommandEditModel
from backend.service.redis_service import RedisService
from backend.utility.server_helper import get_request_ip, get_request_user_agent, prepare_url
from infra_backbone.model.access_log_model import AccessLogModel
from infra_backbone.model.route_model import EnumRouteAccessStrategy
from infra_backbone.model.route_permit_model import EnumRoutePermitResourceCategory
from infra_backbone.service.route_service import RouteService


def process_before_request():
    """
    请求前处理
    :return:
    """
    carrier = MessageCarrier()
    try:
        if request.method in ["OPTIONS"]:
            return
        _check_route_authorization()
        _handle_access_log()

    except ExpiredSignatureError:
        traceback.print_exc()
        raise
    except NotPermissionError as err:
        traceback.print_exc()
        carrier.push_exception(err=err, code=403)
        return jsonify(carrier.dict())
    except NeedLoginError as err:
        traceback.print_exc()
        carrier.push_exception(err=err, code=401)
        return jsonify(carrier.dict())
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
        return jsonify(carrier.dict())


@inject
def _check_route_authorization(
    redis_service: RedisService = Provide[BackendContainer.redis_service],
):
    """
    检查路由权限
    :return:
    """

    def __process_need_authed():
        """
        需要认证过
        :return:
        """
        verify_jwt_in_request()
        redis_service.check_user_profile_by_redis()

    def __process_controlled_role(_auth_list: List[str], _check_url: str):
        """
        验证 角色
        :param _auth_list:
        :return:
        """
        verify_jwt_in_request()
        # _check_master_user_role(role_id_list=_auth_list)

    def __process_controlled_ability_permission(_auth_list: List[str], _check_url: str):
        """
        验证 功能权限
        :param _auth_list:
        :return:
        """
        verify_jwt_in_request()
        # _check_master_user_ability_permission(ability_permission_id_list=_auth_list)

    check_url = get_match_route()
    if not check_url:
        return
    route_dict = current_app.config.get("ROUTE", {})
    route_info = route_dict.get(check_url, None)
    if not route_info:
        return
    if route_info.access_strategy == EnumRouteAccessStrategy.AUTHORIZED.name:
        __process_need_authed()
    if not route_info.permit_list:
        return
    for permit in route_info.permit_list:
        if permit.permitted_resource_category == EnumRoutePermitResourceCategory.ROLE.name:
            __process_controlled_role(
                _auth_list=permit.permitted_resource_ids, _check_url=check_url
            )
        if (
            permit.permitted_resource_category
            == EnumRoutePermitResourceCategory.ABILITY_PERMISSION.name
        ):
            __process_controlled_ability_permission(
                _auth_list=permit.permitted_resource_ids, _check_url=check_url
            )


def _handle_access_log():
    """
    处理访问日志
    :return:
    """
    url_rule = str(request.url_rule)
    exclude_route_list = []
    if url_rule not in exclude_route_list:
        _add_access_log(url_rule=url_rule)


@inject
def _add_access_log(
    url_rule: str,
    pub_client: SyncPubClient = Provide[BackendContainer.pub_client],
):
    request_json = request.get_json(silent=True)
    data = copy.deepcopy(request_json)
    if data is None:
        data = {}
    if "password" in data:
        data.pop("password")

    form_data = request.form.to_dict()
    if form_data:
        data = {**data, **form_data}

    user_agent = get_request_user_agent()
    ip = get_request_ip()

    try:
        visitor_category = get_current_handler().category
        visitor_id = get_current_handler().id
    except Exception:
        visitor_id = None
        visitor_category = None

    files = _get_file_list()
    if isinstance(data, dict) and len(files) > 0:
        data["file_info_list"] = files
    access_log = AccessLogModel(
        visitor_id=visitor_id,
        visitor_category=visitor_category,
        destination=url_rule,
        args=data,
        user_agent=user_agent,
        ip=ip,
        access_on=local_now(),
        footprint=dict(request.headers),
    )
    command = CommandEditModel(category="task_save_access_log", args=access_log)
    pub_client.send_message(message=ORJSONPickle.encode_model(command))


def _get_file_list():
    """
    获取文件列表
    :return:
    """
    file_info_list = []

    files = request.files.getlist("files")
    file = request.files.get("file", None)
    if file:
        files.append(file)

    for file in files:
        file_blob = file.stream.read()
        file_name = file.filename
        size = len(file_blob)
        file.seek(0)
        file_info_list.append({"file_name": file_name, "size": size})
    return file_info_list


def get_match_route() -> Optional[str]:
    """
    获取匹配的路由表达式
    """

    def __match_url(_url_rule):
        """
        检查是否匹配
        :param _url_rule:
        :return:
        """
        if request.url_rule:
            # logging.debug(request.url_rule)
            # 正式环境的context有可能不是从/过来的,需要处理prepare_url
            if request.method in _url_rule.methods and (
                (_url_rule.rule == prepare_url(request.url_rule.rule))
                or (_url_rule.rule == request.url_rule.rule)
            ):
                return True
        return False

    app_url_map_rules = list(current_app.url_map.iter_rules())
    matched_rules = [
        app_url_rule for app_url_rule in app_url_map_rules if __match_url(app_url_rule)
    ]
    # 对于url_rule不区分methods，所以处理第一个即可
    return matched_rules[0].rule if len(matched_rules) > 0 else None


def process_error_handler(error: Exception) -> Any:
    """
    这个handler可以catch住所有的abort(500)和raise exception.
    注入方式：
    app_instance.errorhandler(Exception)(process_error_handler)
    """
    logger.error(error)
    err_info = ErrorInfo.generate_from_err(error)
    carrier = MessageCarrier()
    # 没有捕获到的错误全在在这里扔出
    carrier.push_exception(Exception(f"系统运行遇到未知错误[{err_info.token}]: {err_info.message}"))

    return jsonify(carrier.dict())


@inject
def release_session(
    uow: UnitOfWork = Provide[BackendContainer.uow],
):
    if isinstance(uow, SqlAlchemyUnitOfWork):
        if isinstance(uow.db_session, Session):
            if uow.db_session.in_transaction():
                uow.db_session.commit()
            uow.db_session.close()


def handle_special_errors(response: Response):
    """
    统一处理特殊错误
    :param response:
    :return:
    """
    if not response.data:
        return response
    try:
        data = json.loads(response.data)
        carrier = MessageCarrier(**data)
        if carrier.code == 500:
            if (
                str(EntityNotFoundError) == carrier.error.err_type
                and "version" in carrier.error.message
            ):
                logger.info("EntityNotFoundError原本的错误：%s", carrier.error.message)
                carrier.error.message = "该数据已发生改变，请刷新页面重试，若刷新后依旧错误，请联系管理员！"
                return jsonify(carrier.dict(by_alias=True))
    except Exception as error:
        logger.error(error)
    return response


def process_after_request(response: Response):
    """
    请求后处理
    :return:
    """
    release_session()
    return handle_special_errors(response=response)


@inject
def init_app_process(
    app: Flask,
    uow: UnitOfWork = Provide[BackendContainer.uow],
    route_service: RouteService = Provide[BackendContainer.backbone_container.route_service],
):
    """
    初始化 app 处理
    :return:
    """
    with uow:
        robot = get_robot_handler()
        transaction = uow.log_transaction(
            handler=robot,
            action="refresh_route",
            action_params={},
        )
        flask_app_route_list = list(app.url_map.iter_rules())
        flask_app_route_set = {r.rule for r in flask_app_route_list}
        ignore_path = [
            "/api/web/user/login",
            "/api/web/auth/login",
            "/api/web/auth/get-login-validate-image",
            "/api/favicon.ico",
            "/static/<path:filename>",
            "/api/web/user/get-login-validate-image",
            "/api/web/storage/tinymce-uploads",
            "/api/mobile/auth/dingtalk-login/<string:code>/<string:desired_identity>",
            "/api/mobile/auth/dev-login",
        ]
        route_service.refresh_route(
            flask_app_route_set=flask_app_route_set,
            ignore_path=ignore_path,
            transaction=transaction,
        )
        # 加注路由
        current_app.config["ROUTE"] = route_service.get_route_with_permit()
