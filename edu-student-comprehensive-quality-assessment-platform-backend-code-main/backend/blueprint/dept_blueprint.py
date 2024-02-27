import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.message_carrier import MessageCarrier

from backend.backend_container import BackendContainer
from backend.blueprint import get_current_semester_period_id
from backend.data.constant import FlaskConfigConst
from biz_comprehensive.model.edit.load_class_student_em import LoadClassStudentEditModel
from biz_comprehensive.service.student_points_log_service import StudentPointsLogService
from infra_backbone.service.dept_service import DeptService

blueprint_dept = Blueprint(
    name="dept", import_name=__name__, url_prefix=f"{FlaskConfigConst.API_PREFIX}"
)

MOBILE_PREFIX = "/mobile/dept"


@blueprint_dept.route(f"{MOBILE_PREFIX}/get-info/<string:tree_id>", methods=["POST"])
@inject
def route_get_dept_info(
    tree_id: str,
    dept_service: DeptService = Provide[BackendContainer.backbone_container.dept_service],
):
    """
    获取部门信息
    """
    carrier = MessageCarrier()
    try:
        data = dept_service.get_dept_info_by_tree_id(tree_id=tree_id)
        carrier.push_succeed_data(data=data)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_dept.route(f"{MOBILE_PREFIX}/get-student-list", methods=["POST"])
@inject
def route_get_dept_student_list(
    student_points_log_service: StudentPointsLogService = Provide[
        BackendContainer.comprehensive_container.student_points_log_service
    ],
):
    """
    获取班级学生列表
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        period_id = get_current_semester_period_id()
        data["period_id"] = period_id
        result = student_points_log_service.load_class_student_points(
            data=LoadClassStudentEditModel(**data)
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))
