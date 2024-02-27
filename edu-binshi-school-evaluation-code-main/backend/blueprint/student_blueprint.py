import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.message_carrier import MessageCarrier
from infra_basic.uow_interface import UnitOfWork

from backend.backend_containers import BackendContainer
from backend.blueprint import get_current_handler, get_current_user_id
from backend.data.constant import FlaskConfigConst
from backend.service.app_student_service import AppStudentService
from edu_binshi.data.query_params.student_query_params import StudentPageQueryParams
from edu_binshi.model.edit.student_user_em import StudentUserEm
from edu_binshi.service.student_service import StudentService

blueprint_student = Blueprint(
    name="student",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/student"


@blueprint_student.route(f"{WEB_PREFIX}/get-page", methods=["POST"])
@inject
def route_get_student_page(
    student_service: StudentService = Provide[
        BackendContainer.edu_evaluation_container.student_service
    ],
):
    """
    获取学生分页
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        params = StudentPageQueryParams(**data)
        params.user_id = get_current_user_id()
        result = student_service.get_student_page(
            params=params,
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_student.route(
    f"{WEB_PREFIX}/get-student-info-list-by-establishment-assign-id-list", methods=["POST"]
)
@inject
def route_get_student_info_list_by_establishment_assign_id_list(
    student_service: StudentService = Provide[
        BackendContainer.edu_evaluation_container.student_service
    ],
):
    """
    根据编制分配id列表获取学生信息
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        result = student_service.get_student_info_list_by_establishment_assign_id_list(
            establishment_assign_id_list=data["people_id_list"],
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_student.route(f"{WEB_PREFIX}/get-student-user-page", methods=["POST"])
@inject
def route_get_student_user_page(
    student_service: StudentService = Provide[
        BackendContainer.edu_evaluation_container.student_service
    ],
):
    """
    获取学生分页
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        params = StudentPageQueryParams(**data)
        params.user_id = get_current_user_id()
        result = student_service.get_student_user_page(
            params=params,
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_student.route(f"{WEB_PREFIX}/create-student-user", methods=["POST"])
@inject
def route_create_student_user(
    student_service: StudentService = Provide[
        BackendContainer.edu_evaluation_container.student_service
    ],
    uow: UnitOfWork = Provide[BackendContainer.uow],
):
    """
    创建学生用户
    :param student_service:
    :param uow:
    :return:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        transaction = uow.log_transaction(
            handler=get_current_handler(),
            action="create_student_user",
            action_params=data,
        )
        with uow:
            student_user = StudentUserEm(**data)
            user_id = student_service.create_student_user(
                student_user=student_user,
                transaction=transaction,
            )
        carrier.push_succeed_data(data=user_id)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_student.route(f"{WEB_PREFIX}/batch-create-student-user", methods=["POST"])
@inject
def route_batch_create_student_user(
    student_service: StudentService = Provide[
        BackendContainer.edu_evaluation_container.student_service
    ],
    uow: UnitOfWork = Provide[BackendContainer.uow],
):
    """
    批量创建学生用户
    :param student_service:
    :param uow:
    :return:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        transaction = uow.log_transaction(
            handler=get_current_handler(),
            action="batch_create_student_user",
            action_params=data,
        )
        with uow:
            params = StudentPageQueryParams(**data)
            params.user_id = get_current_user_id()
            user_id = student_service.batch_create_student_user(
                params=params,
                transaction=transaction,
            )
        carrier.push_succeed_data(data=user_id)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_student.route(f"{WEB_PREFIX}/export-student-user", methods=["POST"])
@inject
def route_export_student_user(
    app_student_service: AppStudentService = Provide[BackendContainer.app_student_service],
    uow: UnitOfWork = Provide[BackendContainer.uow],
):
    """
    导出学生用户
    :param app_student_service:
    :param uow:
    :return:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        transaction = uow.log_transaction(
            handler=get_current_handler(),
            action="export_student_user",
            action_params=data,
        )
        with uow:
            params = StudentPageQueryParams(**data)
            params.user_id = get_current_user_id()
            user_id = app_student_service.export_student_user(
                params=params,
                transaction=transaction,
            )
        carrier.push_succeed_data(data=user_id)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))
