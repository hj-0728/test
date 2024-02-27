import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify
from infra_basic.errors import BusinessError
from infra_basic.message_carrier import MessageCarrier

from backend.backend_containers import BackendContainer
from backend.data.constant import FlaskConfigConst
from edu_binshi.service.period_category_service import PeriodCategoryService

blueprint_period_category = Blueprint(
    name="period-category",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/period-category"


@blueprint_period_category.route(f"{WEB_PREFIX}/get-list", methods=["GET"])
@inject
def route_get_period_category_list(
    period_category_service: PeriodCategoryService = Provide[
        BackendContainer.edu_evaluation_container.period_category_service
    ],
):
    """
    获取周期类型列表
    :param period_category_service:
    """
    carrier = MessageCarrier()
    try:
        result = period_category_service.get_period_category_list()
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))
