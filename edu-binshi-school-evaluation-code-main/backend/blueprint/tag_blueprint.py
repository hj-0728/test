import traceback

from dependency_injector.wiring import inject
from flask import Blueprint, jsonify
from infra_basic.errors import BusinessError
from infra_basic.message_carrier import MessageCarrier

from backend.data.constant import FlaskConfigConst
from backend.data.enum import EnumTagName
from infra_utility.enum_helper import enum_to_dict_list

blueprint_tag = Blueprint(
    name="tag",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/tag"


@blueprint_tag.route(f"{WEB_PREFIX}/resource-evaluation-criteria-tree/list", methods=["GET"])
@inject
def route_get_tag_list() -> jsonify:
    """
    获取tag list
    :return:
    """
    carrier = MessageCarrier()
    try:
        data = enum_to_dict_list(EnumTagName)
        carrier.push_succeed_data(data=data)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))
