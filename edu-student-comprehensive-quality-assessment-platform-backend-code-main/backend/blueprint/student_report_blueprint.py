import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.message_carrier import MessageCarrier

from backend.backend_container import BackendContainer
from backend.blueprint import get_current_semester_period_id
from backend.data.constant import FlaskConfigConst
from biz_comprehensive.model.param.student_report_query_params import (
    StudentReportPageFilterParams,
    StudentReportQueryParams,
)
from biz_comprehensive.service.student_report_service import StudentReportService

blueprint_student_report = Blueprint(
    name="student_report", import_name=__name__, url_prefix=f"{FlaskConfigConst.API_PREFIX}"
)

MOBILE_PREFIX = "/mobile/student-report"


@blueprint_student_report.route(
    f"{MOBILE_PREFIX}/get-student-info/<string:establishment_assign_id>", methods=["GET"]
)
@inject
def route_get_student_info(
    establishment_assign_id: str,
    student_report_service: StudentReportService = Provide[
        BackendContainer.comprehensive_container.student_report_service
    ],
):
    """
    获取学生信息
    """
    carrier = MessageCarrier()
    try:
        result = student_report_service.get_student_info(
            establishment_assign_id=establishment_assign_id
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_student_report.route(f"{MOBILE_PREFIX}/get-statistics", methods=["POST"])
@inject
def route_get_student_statistics(
    student_report_service: StudentReportService = Provide[
        BackendContainer.comprehensive_container.student_report_service
    ],
):
    """
    获取学生统计信息
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        data["period_id"] = get_current_semester_period_id()
        result = student_report_service.get_student_statistics(
            params=StudentReportQueryParams(**data)
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_student_report.route(f"{MOBILE_PREFIX}/get-comprehensive-radar-data", methods=["POST"])
@inject
def route_get_student_comprehensive_radar_data(
    student_report_service: StudentReportService = Provide[
        BackendContainer.comprehensive_container.student_report_service
    ],
):
    """
    获取学生综合雷达图数据
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        data["period_id"] = get_current_semester_period_id()
        result = student_report_service.get_student_comprehensive_radar_data(
            params=StudentReportQueryParams(**data)
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_student_report.route(f"{MOBILE_PREFIX}/get-growth-trend-data", methods=["POST"])
@inject
def route_get_student_growth_trend_data(
    student_report_service: StudentReportService = Provide[
        BackendContainer.comprehensive_container.student_report_service
    ],
):
    """
    获取学生成长趋势数据
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        data["period_id"] = get_current_semester_period_id()
        result = student_report_service.get_student_growth_trend_data(
            params=StudentReportQueryParams(**data)
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_student_report.route(f"{MOBILE_PREFIX}/get-observation-scene-list", methods=["POST"])
@inject
def route_get_student_observation_scene_list(
    student_report_service: StudentReportService = Provide[
        BackendContainer.comprehensive_container.student_report_service
    ],
):
    """
    获取观察场景列表
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        data["period_id"] = get_current_semester_period_id()
        result = student_report_service.get_student_observation_scene_list(
            params=StudentReportQueryParams(**data)
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_student_report.route(f"{MOBILE_PREFIX}/get-observation-log-page-list", methods=["POST"])
@inject
def route_get_student_observation_log_page_list(
    student_report_service: StudentReportService = Provide[
        BackendContainer.comprehensive_container.student_report_service
    ],
):
    """
    获取观察日志
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        data["period_id"] = get_current_semester_period_id()
        result = student_report_service.get_student_observation_point_log_page_list(
            params=StudentReportPageFilterParams(**data)
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))
