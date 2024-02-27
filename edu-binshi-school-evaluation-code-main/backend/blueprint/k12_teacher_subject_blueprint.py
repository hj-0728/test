import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.message_carrier import MessageCarrier
from infra_basic.uow_interface import UnitOfWork
from infra_pub_sub_manager.sync_pub_client import SyncPubClient
from infra_utility.serialize_helper import ORJSONPickle

from backend.backend_containers import BackendContainer
from backend.blueprint import get_current_handler
from backend.data.constant import FlaskConfigConst
from backend.model.edit.command_em import CommandEm
from backend.model.edit.command_generate_input_score_log_em import CommandGenerateInputScoreLogEditModel, \
    EnumTriggerCategory
from edu_binshi.data.query_params.teacher_query_params import TeacherPageQueryParams
from edu_binshi.model.edit.k12_teacher_subject_em import K12TeacherSubjectEm
from edu_binshi.service.k12_teacher_subject_service import K12TeacherSubjectService

blueprint_k12_teacher_subject = Blueprint(
    name="k12_teacher_subject",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/k12-teacher-subject"


@blueprint_k12_teacher_subject.route(f"{WEB_PREFIX}/teacher-list", methods=["POST"])
@inject
def route_get_k12_teacher_list_page(
    k12_teacher_subject_service: K12TeacherSubjectService = Provide[
        BackendContainer.edu_evaluation_container.k12_teacher_subject_service
    ],
):
    """
    获取教师列表
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        params = TeacherPageQueryParams(**data)
        result = k12_teacher_subject_service.get_k12_teacher_list_page(
            params=params,
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_k12_teacher_subject.route(f"{WEB_PREFIX}/subject-list", methods=["GET"])
@inject
def route_get_k12_subject_list(
    k12_teacher_subject_service: K12TeacherSubjectService = Provide[
        BackendContainer.edu_evaluation_container.k12_teacher_subject_service
    ],
):
    """
    获取科目列表
    """
    carrier = MessageCarrier()
    try:
        result = k12_teacher_subject_service.get_subject_list()
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_k12_teacher_subject.route(f"{WEB_PREFIX}/save", methods=["POST"])
@inject
def route_set_k12_teacher_subject(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    k12_teacher_subject_service: K12TeacherSubjectService = Provide[
        BackendContainer.edu_evaluation_container.k12_teacher_subject_service
    ],
    pub_client: SyncPubClient = Provide[BackendContainer.pub_client],
):
    """
    设置教师科目
    """
    carrier = MessageCarrier()
    try:
        with uow:
            data = request.get_json(silent=True)
            transaction = uow.log_transaction(
                handler=get_current_handler(),
                action="set_k12_teacher_subject",
                action_params=data
            )
            params = K12TeacherSubjectEm(**data)
            params.update_loop()
            saved, result = k12_teacher_subject_service.save_k12_teacher_subject(
                k12_teacher_subject_em=params,
                transaction=transaction,
            )
        if saved:
            command_args = CommandGenerateInputScoreLogEditModel(
                trigger_category=EnumTriggerCategory.SUBJECT.value,
                trigger_ids=result
            )
            command = CommandEm(category="task_handle_generate_input_score_log", args=command_args)
            pub_client.send_message(message=ORJSONPickle.encode_model(command))
            # 因为返回的result不为空的时候前端有特殊判断，正常保存完没有返回，避免前端判断有误，把result置空
            result = None
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_k12_teacher_subject.route(
    f"{WEB_PREFIX}/detail/<string:people_id>/<string:dimension_dept_tree_id>", methods=["GET"]
)
@inject
def route_get_k12_teacher_subject_detail(
    people_id: str,
    dimension_dept_tree_id: str,
    k12_teacher_subject_service: K12TeacherSubjectService = Provide[
        BackendContainer.edu_evaluation_container.k12_teacher_subject_service
    ],
):
    """
    获取教师科目详情
    """
    carrier = MessageCarrier()
    try:
        result = k12_teacher_subject_service.get_k12_teacher_subject_detail(
            people_id=people_id,
            dimension_dept_tree_id=dimension_dept_tree_id,
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_k12_teacher_subject.route(f"{WEB_PREFIX}/capacity-and-subject-filters", methods=["GET"])
@inject
def route_get_k12_capacity_subject_filters(
    k12_teacher_subject_service: K12TeacherSubjectService = Provide[
        BackendContainer.edu_evaluation_container.k12_teacher_subject_service
    ],
):
    """
    获取科目列表
    """
    carrier = MessageCarrier()
    try:
        result = k12_teacher_subject_service.get_capacity_and_subject_filters()
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))
