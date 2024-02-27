import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.message_carrier import MessageCarrier

from backend.backend_containers import BackendContainer
from backend.blueprint import get_current_people_id, get_current_period_id, get_current_role_code
from backend.data.constant import FlaskConfigConst
from domain_evaluation.data.query_params.evaluation_assignment_query_params import (
    EvaluationAssignmentQueryParams,
)
from domain_evaluation.service.evaluation_assignment_service import EvaluationAssignmentService

blueprint_evaluation_assignment = Blueprint(
    name="evaluation-assignment",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/evaluation-assignment"


@blueprint_evaluation_assignment.route(f"{WEB_PREFIX}/todo-list", methods=["POST"])
@inject
def route_get_evaluation_assignment_todo_list(
    evaluation_assignment_service: EvaluationAssignmentService = Provide[
        BackendContainer.domain_evaluation_container.evaluation_assignment_service
    ],
):
    """
    获取评价分配需要做的列表
    :param evaluation_assignment_service:
    :return:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        params = EvaluationAssignmentQueryParams(**data)
        params.people_id = get_current_people_id()
        params.focus_period_id = get_current_period_id()
        result = evaluation_assignment_service.get_evaluation_assignment_todo_list(
            params=params,
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_assignment.route(f"{WEB_PREFIX}/about-me-list", methods=["POST"])
@inject
def route_get_evaluation_assignment_about_me_list(
    evaluation_assignment_service: EvaluationAssignmentService = Provide[
        BackendContainer.domain_evaluation_container.evaluation_assignment_service
    ],
):
    """
    获取自评的评价分配列表
    :param evaluation_assignment_service:
    :return:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        params = EvaluationAssignmentQueryParams(**data)
        params.people_id = get_current_people_id()
        params.focus_period_id = get_current_period_id()
        result = evaluation_assignment_service.get_evaluation_assignment_about_me_list(
            params=params, current_role_code=get_current_role_code()
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))
