import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.errors import BusinessError
from infra_basic.message_carrier import MessageCarrier

from backend.backend_containers import BackendContainer
from backend.data.constant import FlaskConfigConst
from domain_evaluation.service.score_symbol_service import ScoreSymbolService

blueprint_score_symbol = Blueprint(
    name="score_symbol",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/score-symbol"


@blueprint_score_symbol.route(f"{WEB_PREFIX}/list", methods=["POST"])
@inject
def route_get_score_symbol_list(
    score_symbol_service: ScoreSymbolService = Provide[
        BackendContainer.domain_evaluation_container.score_symbol_service
    ],
) -> jsonify:
    """
    获取score_symbol list
    :return:
    """
    carrier = MessageCarrier()
    try:
        value_type_list = request.json.get("valueTypeList", [])
        data = score_symbol_service.get_score_symbol_list(value_type_list=value_type_list)
        carrier.push_succeed_data(data=data)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))
