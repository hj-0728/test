import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from infra_basic.errors import BusinessError
from infra_basic.message_carrier import MessageCarrier
from infra_basic.uow_interface import UnitOfWork
from infra_pub_sub_manager.sync_pub_client import SyncPubClient
from infra_utility.serialize_helper import ORJSONPickle

from backend.backend_containers import BackendContainer
from backend.blueprint import get_current_handler, get_current_people_id, get_current_period_id, get_current_role_code
from backend.data.constant import FlaskConfigConst
from backend.model.edit.command_em import CommandEm
from backend.service.app_evaluation_criteria_plan_service import AppEvaluationCriteriaPlanService
from domain_evaluation.data.query_params.evaluation_criteria_plan_query_params import (
    EvaluationCriteriaPlanQueryParams,
)
from domain_evaluation.data.query_params.evaluation_criteria_plan_stats_query_params import (
    EvaluationCriteriaPlanStatsQueryParams,
)
from domain_evaluation.model.evaluation_assignment_model import SaveEvaluationAssignmentRelationshipModel
from domain_evaluation.model.evaluation_criteria_plan_model import (
    EvaluationCriteriaPlanModel,
    SaveEvaluationCriteriaPlanAndScopeModel,
    SaveEvaluationCriteriaPlanModel,
)
from domain_evaluation.service.evaluation_criteria_plan_service import EvaluationCriteriaPlanService


blueprint_evaluation_criteria_plan = Blueprint(
    name="evaluation-criteria-plan",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/evaluation-criteria-plan"


@blueprint_evaluation_criteria_plan.route(f"{WEB_PREFIX}/save", methods=["POST"])
@inject
def route_save_evaluation_criteria_plan(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    evaluation_criteria_plan_service: EvaluationCriteriaPlanService = Provide[
        BackendContainer.domain_evaluation_container.evaluation_criteria_plan_service
    ],
):
    """
    保存评价标准计划
    :param uow:
    :param evaluation_criteria_plan_service:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        with uow:
            transaction = uow.log_transaction(
                handler=get_current_handler(),
                action="save_evaluation_criteria_plan",
                action_params={"data": data},
            )
            result = evaluation_criteria_plan_service.save_evaluation_criteria_plan(
                evaluation_criteria_plan=SaveEvaluationCriteriaPlanModel(**data),
                transaction=transaction,
            )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria_plan.route(f"{WEB_PREFIX}/list", methods=["POST"])
@jwt_required()
@inject
def route_get_evaluation_criteria_plan_list(
    evaluation_criteria_plan_service: EvaluationCriteriaPlanService = Provide[
        BackendContainer.domain_evaluation_container.evaluation_criteria_plan_service
    ],
):
    """
    获取评价计划列表
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        params = EvaluationCriteriaPlanQueryParams(**data)
        params.period_id = get_current_period_id()
        result = evaluation_criteria_plan_service.get_evaluation_criteria_plan_list(
            params=params,
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria_plan.route(
    f"{WEB_PREFIX}/get-detail/<string:evaluation_criteria_plan_id>", methods=["GET"]
)
@inject
def route_get_evaluation_criteria_plan_detail(
    evaluation_criteria_plan_id: str,
    evaluation_criteria_plan_service: EvaluationCriteriaPlanService = Provide[
        BackendContainer.domain_evaluation_container.evaluation_criteria_plan_service
    ],
):
    """
    获取评价标准计划详情
    :param evaluation_criteria_plan_id:
    :param evaluation_criteria_plan_service:
    """
    carrier = MessageCarrier()
    try:
        result = evaluation_criteria_plan_service.get_evaluation_criteria_plan_detail(
            evaluation_criteria_plan_id=evaluation_criteria_plan_id,
        )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria_plan.route(f"{WEB_PREFIX}/abolish", methods=["POST"])
@inject
def route_abolish_evaluation_criteria_plan(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    evaluation_criteria_plan_service: EvaluationCriteriaPlanService = Provide[
        BackendContainer.domain_evaluation_container.evaluation_criteria_plan_service
    ],
):
    """
    将评价计划状态改为作废
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        with uow:
            transaction = uow.log_transaction(
                handler=get_current_handler(),
                action="abolish_evaluation_criteria_plan",
                action_params={"data": data},
            )
            result = evaluation_criteria_plan_service.update_evaluation_criteria_plan(
                evaluation_criteria_plan=EvaluationCriteriaPlanModel(**data),
                trans=transaction,
            )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria_plan.route(f"{WEB_PREFIX}/delete", methods=["POST"])
@inject
def route_delete_evaluation_criteria_plan(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    evaluation_criteria_plan_service: EvaluationCriteriaPlanService = Provide[
        BackendContainer.domain_evaluation_container.evaluation_criteria_plan_service
    ],
):
    """
    删除评价计划
    :param uow:
    :param evaluation_criteria_plan_service:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        with uow:
            transaction = uow.log_transaction(
                handler=get_current_handler(),
                action="delete_evaluation_criteria_plan",
                action_params={"data": data},
            )
            result = evaluation_criteria_plan_service.delete_evaluation_criteria_plan(
                evaluation_criteria_plan_id=data.get("evaluationCriteriaId"),
                transaction=transaction,
            )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria_plan.route(f"{WEB_PREFIX}/todo-list", methods=["POST"])
@inject
def route_get_evaluation_criteria_plan_todo_page_list(
    evaluation_criteria_plan_service: EvaluationCriteriaPlanService = Provide[
        BackendContainer.domain_evaluation_container.evaluation_criteria_plan_service
    ],
):
    """
    获取评价列表
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        params = EvaluationCriteriaPlanStatsQueryParams(**data)
        params.people_id = get_current_people_id()
        params.focus_period_id = get_current_period_id()
        result = evaluation_criteria_plan_service.get_evaluation_criteria_plan_todo_page_list(
            params=params, current_role_code=get_current_role_code()
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria_plan.route(f"{WEB_PREFIX}/save-plan-and-scope", methods=["POST"])
@inject
def route_save_evaluation_criteria_plan_and_scope(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    app_evaluation_criteria_plan_service: AppEvaluationCriteriaPlanService = Provide[
        BackendContainer.app_evaluation_criteria_plan_service
    ],
    pub_client: SyncPubClient = Provide[BackendContainer.pub_client],
):
    """
    保存评价标准计划和计划适用范围
    :param uow:
    :param app_evaluation_criteria_plan_service:
    :param pub_client:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        with uow:
            transaction = uow.log_transaction(
                handler=get_current_handler(),
                action="save_evaluation_criteria_plan_and_scope",
                action_params={"data": data},
            )
            evaluation_criteria_plan_vm, evaluation_criteria_plan_scope_list = app_evaluation_criteria_plan_service.save_evaluation_criteria_plan_and_scope(
                data=SaveEvaluationCriteriaPlanAndScopeModel(**data),
                transaction=transaction,
            )
        if evaluation_criteria_plan_vm.status == "PUBLISHED":
            command_args = SaveEvaluationAssignmentRelationshipModel(
                evaluation_criteria_plan=evaluation_criteria_plan_vm,
                evaluation_criteria_plan_scope_list=evaluation_criteria_plan_scope_list
            )
            command = CommandEm(category="task_save_evaluation_assignment_relationship", args=command_args)
            pub_client.send_message(message=ORJSONPickle.encode_model(command))
        carrier.push_succeed_data()
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria_plan.route(
    f"{WEB_PREFIX}/get-info-by-id/<string:evaluation_criteria_plan_id>", methods=["GET"]
)
@inject
def route_get_evaluation_criteria_plan_info(
    evaluation_criteria_plan_id: str,
    evaluation_criteria_plan_service: EvaluationCriteriaPlanService = Provide[
        BackendContainer.domain_evaluation_container.evaluation_criteria_plan_service
    ],
):
    """
    获取评价标准计划本身信息
    :param evaluation_criteria_plan_id:
    :param evaluation_criteria_plan_service:
    """
    carrier = MessageCarrier()
    try:
        result = evaluation_criteria_plan_service.get_evaluation_criteria_plan(
            plan_id=evaluation_criteria_plan_id,
        )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))
