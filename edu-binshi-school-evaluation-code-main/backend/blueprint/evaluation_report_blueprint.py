import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.message_carrier import MessageCarrier
from infra_basic.uow_interface import UnitOfWork
from infra_pub_sub_manager.sync_pub_client import SyncPubClient
from infra_utility.serialize_helper import ORJSONPickle
from infra_utility.token_helper import generate_uuid_id

from backend.backend_containers import BackendContainer
from backend.blueprint import (
    get_current_handler,
    get_current_people_id,
    get_current_role_code,
    get_current_role_id,
    get_current_user_id, get_current_user_role,
)
from backend.data.constant import FlaskConfigConst
from backend.data.query_params.evaluation_report_assignment_query_params import (
    EvaluationReportAssignmentQueryParams,
)
from backend.model.edit.command_em import CommandEm
from backend.service.evaluation_report_service import EvaluationReportService
from edu_binshi.model.edit.evaluation_report_dept_tree_em import EvaluationReportDeptTreeEditModel
from edu_binshi.model.report_record_model import ReportRecordModel, \
    EnumReportRecordStatus
from edu_binshi.model.view.report_record_vm import ReportRecordViewModel
from edu_binshi.service.report_service import ReportService

blueprint_evaluation_report = Blueprint(
    name="evaluation-report",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/evaluation-report"


@blueprint_evaluation_report.route(f"{WEB_PREFIX}/tree", methods=["POST"])
@inject
def route_get_evaluation_report_tree(
    evaluation_report_service: EvaluationReportService = Provide[
        BackendContainer.evaluation_report_service
    ],
):
    """
    获取评价列表
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        data["current_people_id"] = get_current_people_id()
        data["current_role_code"] = get_current_role_code()
        params = EvaluationReportDeptTreeEditModel(**data)
        result = evaluation_report_service.get_evaluation_report_tree(params=params)
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_report.route(f"{WEB_PREFIX}/assignment-page-list", methods=["POST"])
@inject
def route_get_evaluation_report_assignment_page_list(
    evaluation_report_service: EvaluationReportService = Provide[
        BackendContainer.evaluation_report_service
    ],
):
    """
    获取评价列表
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        data["current_people_id"] = get_current_people_id()
        data["current_role_code"] = get_current_role_code()
        params = EvaluationReportAssignmentQueryParams(**data)
        result = evaluation_report_service.get_evaluation_report_assignment(params=params)
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_report.route(
    f"{WEB_PREFIX}/get-evaluation-assignment-report", methods=["POST"]
)
@inject
def route_get_evaluation_assignment_report(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    report_service: ReportService = Provide[
        BackendContainer.edu_evaluation_container.report_service,
    ],
):
    """
    获取学生报告
    """
    carrier = MessageCarrier()
    try:
        with uow:
            data = request.get_json(silent=True)
            data["role_id"] = get_current_role_id()
            data["user_id"] = get_current_user_id()
            data["user_role_id"] = get_current_user_role().id
            data["status"] = EnumReportRecordStatus.PENDING.name
            transaction = uow.log_transaction(
                handler=get_current_handler(),
                action="get_evaluation_assignment_report",
                action_params={"data": data},
            )
            args = ReportRecordViewModel(**data)
            file_info = report_service.before_generate_report_check(
                args=args,
                transaction=transaction
            )
            if not file_info:
                file_info, _ = report_service.generate_report(
                    report_record=args,
                    transaction=transaction,
                )
        carrier.push_succeed_data(data=file_info)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_report.route(f"{WEB_PREFIX}/get-dimension-dept-tree-report", methods=["POST"])
@inject
def route_get_dimension_dept_tree_report(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    report_service: ReportService = Provide[
        BackendContainer.edu_evaluation_container.report_service,
    ],
    pub_client: SyncPubClient = Provide[BackendContainer.pub_client],
):
    """
    获取部门树上的报告
    :param uow:
    :param report_service:
    :param pub_client:
    :return:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        data["current_people_id"] = get_current_people_id()
        data["current_role_code"] = get_current_role_code()
        data["role_id"] = get_current_role_id()
        data["user_id"] = get_current_user_id()
        data["user_role_id"] = get_current_user_role().id
        data["status"] = EnumReportRecordStatus.PENDING.name
        args = ReportRecordViewModel(**data)
        with uow:
            transaction = uow.log_transaction(
                handler=get_current_handler(),
                action="save_report_record",
                action_params={"data": data},
            )
            args.id = generate_uuid_id()
            file_info = report_service.before_generate_report_check(
                args=args,
                transaction=transaction
            )
        if not file_info:
            command_args = args
            command = CommandEm(
                category="task_get_dimension_dept_tree_report",
                args=command_args,
            )
            pub_client.send_message(message=ORJSONPickle.encode_model(command))
        carrier.push_succeed_data(data=file_info)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))
