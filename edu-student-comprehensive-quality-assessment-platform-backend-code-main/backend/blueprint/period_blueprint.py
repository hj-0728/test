import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.message_carrier import MessageCarrier

from backend.backend_container import BackendContainer
from backend.data.constant import FlaskConfigConst
from biz_comprehensive.service.period_service import PeriodService

blueprint_period = Blueprint(
    name="period", import_name=__name__, url_prefix=f"{FlaskConfigConst.API_PREFIX}"
)

MOBILE_PREFIX = "/mobile/period"


@blueprint_period.route(f"{MOBILE_PREFIX}/get-period-category-date", methods=["POST"])
@inject
def route_get_period_category_date(
    period_service: PeriodService = Provide[
        BackendContainer.comprehensive_container.period_service
    ],
):
    """
    获取部门信息
    """
    carrier = MessageCarrier()
    try:
        mini_period_category = request.args.get("miniPeriodCategory")
        data = period_service.get_period_category_date(mini_period_category=mini_period_category)
        carrier.push_succeed_data(data=data)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))
