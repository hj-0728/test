import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.errors import BusinessError
from infra_basic.message_carrier import MessageCarrier
from infra_basic.uow_interface import UnitOfWork

from backend.backend_containers import BackendContainer
from backend.blueprint import get_current_handler, get_current_user_id
from backend.data.constant import FlaskConfigConst
from backend.service.app_role_service import AppRoleService
from infra_backbone.model.params.site_message_query_params import SiteMessageQueryParams
from infra_backbone.service.site_message_service import SiteMessageService

blueprint_site_message = Blueprint(
    name="site_message",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/site-message"


@blueprint_site_message.route(f"{WEB_PREFIX}/unread-exist", methods=["GET"])
@inject
def route_judge_unread_message_exist(
    site_message_service: SiteMessageService = Provide[
        BackendContainer.backbone_container.site_message_service
    ],
    role_service: AppRoleService = Provide[BackendContainer.app_role_service],
):
    """
    是否存在未读消息
    """
    carrier = MessageCarrier()
    try:
        exist_unread_message_count = site_message_service.check_has_unread_message(
            user_id=get_current_user_id(),
            role_id=role_service.get_current_role_id(),
        )
        carrier.push_succeed_data(data=exist_unread_message_count)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict())


@blueprint_site_message.route(f"{WEB_PREFIX}/list", methods=["POST"])
@inject
def route_get_site_message_list_page_info(
    site_message_service: SiteMessageService = Provide[
        BackendContainer.backbone_container.site_message_service
    ],
    role_service: AppRoleService = Provide[BackendContainer.app_role_service],
):
    """
    获取站内信列表页数据
    """
    carrier = MessageCarrier()
    try:
        params = request.get_json(silent=True)
        params["user_id"] = get_current_user_id()
        params["role_id"] = role_service.get_current_role_id()
        query_param = SiteMessageQueryParams(**params)
        result = site_message_service.get_site_message_list_page_info(query_params=query_param)
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_site_message.route(f"{WEB_PREFIX}/info/<string:site_message_id>", methods=["GET"])
@inject
def route_get_site_message_info(
    site_message_id: str,
    site_message_service: SiteMessageService = Provide[
        BackendContainer.backbone_container.site_message_service
    ],
    uow: UnitOfWork = Provide[BackendContainer.uow],
):
    """
    获取消息信息
    """
    carrier = MessageCarrier()
    try:
        with uow:
            transaction = uow.log_transaction(
                handler=get_current_handler(),
                action="read_message",
                action_params={"site_message_id": site_message_id},
            )
            result = site_message_service.get_site_message_info(
                site_message_id=site_message_id,
                transaction=transaction,
            )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_site_message.route(f"{WEB_PREFIX}/read/<string:site_message_id>", methods=["POST"])
@inject
def route_read_site_message(
    site_message_id: str,
    site_message_service: SiteMessageService = Provide[
        BackendContainer.backbone_container.site_message_service
    ],
    uow: UnitOfWork = Provide[BackendContainer.uow],
):
    """
    阅读消息信息
    """
    carrier = MessageCarrier()
    try:
        transaction = uow.log_transaction(
            handler=get_current_handler(),
            action="read_site_message",
            action_params={"site_message_id": site_message_id},
        )
        result = site_message_service.read_site_message(
            site_message_id=site_message_id,
            transaction=transaction,
        )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))
