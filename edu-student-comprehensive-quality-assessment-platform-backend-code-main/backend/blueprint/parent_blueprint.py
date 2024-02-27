import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify
from infra_basic.message_carrier import MessageCarrier

from backend.backend_container import BackendContainer
from backend.blueprint import get_current_people_id
from backend.data.constant import FlaskConfigConst
from biz_comprehensive.service.parent_service import ParentService

parent_blueprint = Blueprint(
    name="parent", import_name=__name__, url_prefix=f"{FlaskConfigConst.API_PREFIX}"
)

MOBILE_PREFIX = "/mobile/parent"


@parent_blueprint.route(f"{MOBILE_PREFIX}/get-child-list", methods=["GET"])
@inject
def route_get_child_list(
    parent_service: ParentService = Provide[
        BackendContainer.comprehensive_container.parent_service
    ],
):
    """
    获取子项列表
    """
    carrier = MessageCarrier()
    try:
        data = parent_service.get_child_list(parent_people_id=get_current_people_id())
        carrier.push_succeed_data(data=data)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))
