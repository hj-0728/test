import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.message_carrier import MessageCarrier

from backend.backend_container import BackendContainer
from backend.blueprint import get_current_people_id, get_current_semester_period_id
from backend.data.constant import FlaskConfigConst
from biz_comprehensive.model.param.class_report_query_params import (
    ClassReportPageFilterParams,
    ClassReportQueryParams,
)
from biz_comprehensive.service.class_report_service import ClassReportService

blueprint_class_report = Blueprint(
    name="class_report", import_name=__name__, url_prefix=f"{FlaskConfigConst.API_PREFIX}"
)

MOBILE_PREFIX = "/mobile/class-report"


@blueprint_class_report.route(f"{MOBILE_PREFIX}/get-class-points-count", methods=["POST"])
@inject
def route_get_class_points_count(
    class_report_service: ClassReportService = Provide[
        BackendContainer.comprehensive_container.class_report_service
    ],
):
    """
    获取班级积分数
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        data["period_id"] = get_current_semester_period_id()
        result = class_report_service.get_class_observation_points_count(
            params=ClassReportQueryParams(**data)
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_class_report.route(f"{MOBILE_PREFIX}/get-ranking", methods=["POST"])
@inject
def route_get_ranking(
    class_report_service: ClassReportService = Provide[
        BackendContainer.comprehensive_container.class_report_service
    ],
):
    """
    获取班级排行榜
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        data["period_id"] = get_current_semester_period_id()
        result = class_report_service.get_class_ranking(params=ClassReportQueryParams(**data))
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_class_report.route(f"{MOBILE_PREFIX}/get-observation-teacher", methods=["POST"])
@inject
def route_get_observation_teacher(
    class_report_service: ClassReportService = Provide[
        BackendContainer.comprehensive_container.class_report_service
    ],
):
    """
    获取观察的老师
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        data["period_id"] = get_current_semester_period_id()
        result = class_report_service.get_observation_teacher(
            params=ClassReportQueryParams(**data), current_people_id=get_current_people_id()
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_class_report.route(f"{MOBILE_PREFIX}/get-observation-log-page-list", methods=["POST"])
@inject
def route_get_observation_log_page_list(
    class_report_service: ClassReportService = Provide[
        BackendContainer.comprehensive_container.class_report_service
    ],
):
    """
    获取观察日志
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        data["period_id"] = get_current_semester_period_id()
        result = class_report_service.get_observation_log_page_list(
            params=ClassReportPageFilterParams(**data), current_people_id=get_current_people_id()
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))
