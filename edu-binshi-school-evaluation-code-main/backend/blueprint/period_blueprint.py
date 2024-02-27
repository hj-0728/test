import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from infra_basic.errors import BusinessError
from infra_basic.message_carrier import MessageCarrier

from backend.backend_containers import BackendContainer
from backend.data.constant import FlaskConfigConst
from backend.model.view.period_vm import PeriodVm
from backend.service.period_service import PeriodService as BackendPeriodService
from backend.service.redis_service import RedisService
from edu_binshi.repository.period_repository import PeriodRepository
from edu_binshi.service.period_service import PeriodService

blueprint_period = Blueprint(
    name="period",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/period"


@blueprint_period.route(f"{WEB_PREFIX}/get-tree", methods=["POST"])
@inject
def route_get_period_tree(
    period_service: PeriodService = Provide[
        BackendContainer.edu_evaluation_container.period_service
    ],
):
    """
    获取周期树
    :param period_service:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        result = period_service.get_period_tree(
            period_category_code=data.get("periodCategoryCode"),
        )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_period.route(f"{WEB_PREFIX}/current-period", methods=["GET"])
@jwt_required()
@inject
def route_get_current_period(
    period_service: BackendPeriodService = Provide[BackendContainer.period_service],
):
    """
    获取当前周期
    :param period_service:
    :return:
    """
    carrier = MessageCarrier()
    try:
        result = period_service.get_current_period()
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_period.route(f"{WEB_PREFIX}/get-list/<string:category>", methods=["GET"])
@inject
def route_get_period_list_by_category(
    category: str,
    period_repository: PeriodRepository = Provide[
        BackendContainer.edu_evaluation_container.period_repository
    ],
):
    """
    根据周期类型获取周期列表
    :param category:
    :param period_repository:
    :return:
    """
    carrier = MessageCarrier()
    try:
        result = period_repository.get_period_list_by_category_code(
            period_category_code=category,
        )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_period.route(f"{WEB_PREFIX}/change-current-period", methods=["POST"])
@inject
def route_change_current_period(
    redis_service: RedisService = Provide[BackendContainer.redis_service],
):
    """
    切换当前周期
    :param redis_service:
    :return:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        redis_service.set_redis_period(
            period_profile=PeriodVm(**data),
        )
        carrier.push_succeed_data(data=True)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))
