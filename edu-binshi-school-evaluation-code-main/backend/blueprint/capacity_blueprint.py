import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify
from infra_basic.message_carrier import MessageCarrier

from backend.backend_containers import BackendContainer
from backend.blueprint import get_current_dd_remote_user_id, get_dingtalk_corp_id
from backend.data.constant import FlaskConfigConst
from backend.service.redis_service import RedisService

blueprint_capacity = Blueprint(
    name="capacity",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

DINGTALK_PREFIX = "/dingtalk/capacity"


@blueprint_capacity.route(
    f"{DINGTALK_PREFIX}/switch-capacity/<string:capacity_code>", methods=["GET"]
)
@inject
def route_switch_dingtalk_user_capacity(
    capacity_code: str,
    redis_service: RedisService = Provide[BackendContainer.redis_service],
) -> jsonify:
    """
    切换dingtalk用户当前capacity
    :return:
    """
    carrier = MessageCarrier()
    try:
        redis_service.update_redis_user_profile_current_capacity_for_mobile(
            capacity_code=capacity_code,
            remote_user_id=get_current_dd_remote_user_id(),
            dingtalk_corp_id=get_dingtalk_corp_id(),
        )
        carrier.push_succeed_data(data=True)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict())
