"""
用户 蓝图层
"""

import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.basic_repository import PageFilterParams
from infra_basic.errors import BusinessError
from infra_basic.message_carrier import MessageCarrier

from backend.backend_containers import BackendContainer
from backend.blueprint import get_current_dd_remote_user_id, get_dingtalk_corp_id
from backend.data.constant import FlaskConfigConst
from backend.service.app_dingtalk_user_service import AppDingtalkUserService
from infra_dingtalk.service.dingtalk_user_service import DingtalkUserService

blueprint_dingtalk_user = Blueprint(
    name="dingtalk_user",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/dingtalk-user"
dingtalk_PREFIX = "/dingtalk/dingtalk-user"


@blueprint_dingtalk_user.route(f"{WEB_PREFIX}/list", methods=["POST"])
@inject
def route_get_people_list(
    dingtalk_user_service: DingtalkUserService = Provide[
        BackendContainer.dingtalk_container.dingtalk_user_service
    ],
):
    """ "
    获取钉钉列表
    """
    carrier = MessageCarrier()
    try:
        query_params = request.get_json(silent=True)
        result = dingtalk_user_service.get_dingtalk_user_list(
            query_params=PageFilterParams(**query_params), dingtalk_corp_id=get_dingtalk_corp_id()
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_dingtalk_user.route(f"{dingtalk_PREFIX}/info", methods=["GET"])
@inject
def route_get_dingtalk_user_info(
    dingtalk_user_service: AppDingtalkUserService = Provide[
        BackendContainer.app_dingtalk_user_service
    ],
):
    """
    获取人员信息
    :return:
    """
    carrier = MessageCarrier()
    try:
        data = dingtalk_user_service.get_dingtalk_user_info(
            remote_user_id=get_current_dd_remote_user_id(),
            dingtalk_corp_id=get_dingtalk_corp_id(),
        )
        carrier.push_succeed_data(data=data)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))
