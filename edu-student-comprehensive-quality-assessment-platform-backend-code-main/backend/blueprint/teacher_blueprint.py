import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.errors import BusinessError
from infra_basic.message_carrier import MessageCarrier
from infra_basic.uow_interface import UnitOfWork

from backend.backend_container import BackendContainer
from backend.blueprint import (
    get_current_handler,
    get_current_people_id,
    get_current_semester_period,
    get_current_semester_period_id,
)
from backend.data.constant import FlaskConfigConst
from biz_comprehensive.model.param.teacher_observation_query_params import (
    TeacherObservationQueryParams,
)
from biz_comprehensive.service.teacher_service import TeacherService

blueprint_teacher = Blueprint(
    name="teacher", import_name=__name__, url_prefix=f"{FlaskConfigConst.API_PREFIX}"
)

MOBILE_PREFIX = "/mobile/teacher"


@blueprint_teacher.route(f"{MOBILE_PREFIX}/get-info", methods=["GET"])
@inject
def route_get_teacher_info(
    teacher_service: TeacherService = Provide[
        BackendContainer.comprehensive_container.teacher_service
    ],
):
    """
    获取教师信息
    """
    carrier = MessageCarrier()
    try:
        people_id = get_current_people_id()
        teacher = teacher_service.get_teacher_info(
            people_id=people_id, period=get_current_semester_period()
        )
        carrier.push_succeed_data(data=teacher)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_teacher.route(f"{MOBILE_PREFIX}/get-taught-class", methods=["GET"])
@inject
def route_get_taught_class(
    teacher_service: TeacherService = Provide[
        BackendContainer.comprehensive_container.teacher_service
    ],
) -> jsonify:
    """
    获取任教班级
    """
    carrier = MessageCarrier()
    try:
        teacher_id = get_current_people_id()
        period_id = get_current_semester_period_id()
        teacher_list = teacher_service.get_teacher_class_list(
            teacher_id=teacher_id, period_id=period_id
        )
        carrier.push_succeed_data(data=teacher_list)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_teacher.route(f"{MOBILE_PREFIX}/get-grade-class-list", methods=["GET"])
@inject
def route_get_grade_class_list(
    teacher_service: TeacherService = Provide[
        BackendContainer.comprehensive_container.teacher_service
    ],
) -> jsonify:
    """
    获取年级班级列表
    """
    carrier = MessageCarrier()
    try:
        grade_class_list = teacher_service.get_school_grade_class_list()
        carrier.push_succeed_data(data=grade_class_list)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_teacher.route(f"{MOBILE_PREFIX}/search-student", methods=["POST"])
@inject
def route_search_school_student(
    teacher_service: TeacherService = Provide[
        BackendContainer.comprehensive_container.teacher_service
    ],
    uow: UnitOfWork = Provide[BackendContainer.uow],
):
    """
    搜索学生
    """
    carrier = MessageCarrier()
    try:
        search_text = request.get_json(silent=True).get("searchText")
        if not search_text:
            carrier.push_succeed_data(data=[])
            return jsonify(carrier.dict(by_alias=True))
        transaction = uow.log_transaction(
            handler=get_current_handler(),
            action="search_school_student",
            action_params={"search_text": search_text},
        )
        with uow:
            student_list = teacher_service.search_student(
                people_id=get_current_people_id(), search_text=search_text, transaction=transaction
            )
        carrier.push_succeed_data(data=student_list)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_teacher.route(f"{MOBILE_PREFIX}/get-observation-class-list", methods=["POST"])
@inject
def route_get_observation_class_list(
    teacher_service: TeacherService = Provide[
        BackendContainer.comprehensive_container.teacher_service
    ],
) -> jsonify:
    """
    获取观察班级列表
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        data["people_id"] = get_current_people_id()
        data["period_id"] = get_current_semester_period_id()
        observation_class_list = teacher_service.get_observation_class_list(
            params=TeacherObservationQueryParams(**data)
        )
        carrier.push_succeed_data(data=observation_class_list)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))
